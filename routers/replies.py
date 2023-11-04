from fastapi import APIRouter, Depends, Query, Path, Request, Response, status
from datetime import datetime
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from common.auth import get_current_user, oauth2_scheme
from models.reply import Reply, Vote
from common.reply_responses import (create_reply_response, choose_best_reply_response,
                                    vote_response, edit_reply_response)
from common.responses import InternalServerError, Locked, NotFound, BestReplyExists
from services import replies_services as rs

replies_router = APIRouter(prefix='/replies')
templates = Jinja2Templates(directory="templates")


@replies_router.get('/create', response_class=HTMLResponse)
async def search(request: Request):
    return templates.TemplateResponse("reply_templates/create_reply.html", {"request": request})


@replies_router.post('/{topic_id}', status_code=status.HTTP_200_OK, responses=create_reply_response)
async def create_reply(
        topic_id: Annotated[int, Path(
                            description='The ID of the topic you want to reply to')],
        content: Annotated[str, Query(
                            min_length=10, max_length=1000, 
                            description='Enter text between [10 | 1000] symbols')],
        token: Annotated[str, Depends(oauth2_scheme)],
        ) -> Reply or NotFound:
    
    user = await get_current_user(token)
    existing_topic = rs.topic_exists(topic_id)

    if not existing_topic:
        return NotFound(content=f'Topic {topic_id} doesn\'t exist')
        
    if rs.topic_is_locked(existing_topic.id):
        return Locked(content=f'Topic {existing_topic.id} is locked!')
    
    if not rs.user_has_write_access(existing_topic, user):
        return Response(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content='User has no write access to that category!'
                    )
    
    new_reply = Reply(topic_id=existing_topic.id, 
                      content=content, 
                      user_id=user.id, 
                      created_on=datetime.utcnow()
                    )
    return rs.create_reply(new_reply)
    

@replies_router.patch('/{topic_id}/reply/{reply_id}', 
                      status_code=status.HTTP_200_OK, 
                      responses=choose_best_reply_response)
async def choose_best_reply(
        topic_id: Annotated[int, Path(description='The ID of the topic')],
        reply_id: Annotated[int, Path(description='The ID of the reply you want to choose')],
        token: Annotated[str, Depends(oauth2_scheme)],
        ) -> Reply or NotFound:
    '''choose best reply 
        /only the author of the topic can do it/'''
    
    user = await get_current_user(token)
    existing_topic = rs.topic_exists(topic_id)
    if not existing_topic:
        return NotFound(content=f'Topic {topic_id} doesn\'t exist')
    
    if not existing_topic.author_id == user.id:
        return Response(status_code=status.HTTP_403_FORBIDDEN, 
                        content='You are not the author of this topic!')
    
    if rs.topic_has_best_reply(existing_topic):
        return BestReplyExists(content='This topic already has a best reply')
    
    existing_reply = rs.get_reply_by_id(topic_id, reply_id)
    
    if not existing_reply:
        return NotFound(content=f'Reply {reply_id} doesn\'t exist')
    
    result = rs.choose_best(existing_reply, existing_topic.id)
    if result: existing_reply.is_best = True
    return existing_reply if result else InternalServerError


@replies_router.put('/{reply_id}/reply/{topic_id}', 
                    status_code=status.HTTP_202_ACCEPTED, 
                    responses=vote_response)
async def vote(
        reply_id: Annotated[int, Path(description='The ID of the reply you want to vote for')],
        topic_id: Annotated[int, Path(description='The ID of the topic')],
        vote: Annotated[Vote, Query(description='Choose action: up, down, remove')],
        token: Annotated[str, Depends(oauth2_scheme)],
        ) -> Reply or NotFound:
    '''upvote/downvote/remove vote for a specific reply'''

    user = await get_current_user(token)
    existing_reply = rs.get_reply_by_id(topic_id, reply_id)
    if not existing_reply:
        return NotFound(content=f'Reply {reply_id} doesn\'t exist')
    
    votes_result = rs.check_user_vote_for_reply(user.id, existing_reply, vote)
    if votes_result:
        upvotes, downvotes = votes_result
        return Response(
                status_code=status.HTTP_202_ACCEPTED,
                content=
                f'Reply {existing_reply.id}: upvotes {upvotes}:{downvotes} downvotes')
    
    return Response(status_code=status.HTTP_200_OK, content='No vote to remove')


@replies_router.put('/{topic_id}/reply/{reply_id}', 
                    status_code=status.HTTP_205_RESET_CONTENT, 
                    responses=edit_reply_response)
async def edit_reply(
        topic_id: Annotated[int, Path(description='The ID of the topic')],
        reply_id: Annotated[int, Path(description='The ID of the reply you want to edit')], 
        token: Annotated[str, Depends(oauth2_scheme)],
        new_content: Annotated[str | None, 
                               Query(min_length=10, 
                                    max_length=1000,
                                    description='Edit content between [10 | 1000] symbols')] = None
        ) -> Reply or NotFound:
    
    user = await get_current_user(token)
    if not rs.topic_exists(topic_id):
        return NotFound(content=f'Topic {topic_id} doesn\'t exist')
    
    existing_reply = rs.get_reply_by_id(topic_id, reply_id)
    if not existing_reply:
        return NotFound(content=f'Reply {reply_id} doesn\'t exist')
    
    if existing_reply.user_id != user.id:
        return Response(status_code=status.HTTP_403_FORBIDDEN, 
                        content='You are not the author of this reply!')
    
    result = rs.edit_reply(existing_reply, new_content)
    if result: existing_reply.content = new_content
        
    return existing_reply if result else InternalServerError