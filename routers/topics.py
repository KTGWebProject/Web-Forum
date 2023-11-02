from datetime import datetime

from fastapi.templating import Jinja2Templates
from common.auth import get_current_user, oauth2_scheme
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, Response, status, Request
from fastapi.responses import JSONResponse
from models.reply import Reply
from models.topic import Topic
from common.responses import BadRequest, Locked, NotFound
from common.topic_responses import (create_topic_response, view_all_topics_response, count_topics_response, 
                                    view_topic_by_id_response, edit_topic_response, lock_topic_response)
from mariadb import _mariadb as mdb
from models.user import User
from services import topics_services as ts

topics_router = APIRouter(prefix="/topics")

templates = Jinja2Templates(directory="templates")

@topics_router.get('/', response_model=list[Topic|Reply], responses=view_all_topics_response) 
async def view_all(
    request = Request,
    search: Annotated[str | None, Query(min_length=3, max_length=30)] = [],
    include_topics: Annotated[bool, Query] = True,
    include_replies: Annotated[bool, Query] = True,
    sort_oldest_first: Annotated[bool, Query] = False,
    paginated: Annotated[bool, Query] = True,
    page: Annotated[int, Query] = 1,
    ) -> list[Topic|Reply]: 
    token = request.cookies.get("access_token")

    '''Responds with a list of Topic resources'''

    blacklist = {'and', 'but', 'from', 'only', 'top'}
    if search:
        search = set(word for word in search.split()).difference(blacklist)

    try:
        user = await get_current_user(token)
        result = ts.view_all_topics(user=user, 
                                    search_in_title=search, 
                                    include_topics=include_topics, 
                                    include_replies=include_replies, 
                                    sort_by_date=sort_oldest_first, 
                                    paginated=paginated, 
                                    default_page=page) 
    except:
        result = ts.view_all_topics(search_in_title=search, 
                                    include_topics=include_topics, 
                                    include_replies=include_replies, 
                                    sort_by_date=sort_oldest_first, 
                                    paginated=paginated, 
                                    default_page=page
                                    )
    return templates.TemplateResponse("list_topics.html", {"request": request, "topics": result})

@topics_router.get('/count/{category_id}', responses=count_topics_response)
def topics_count(category_id: int) -> int:
    '''Helping function to define the pages in the forum client'''
    return ts._count_topics(category_id)[0]


@topics_router.get('/{id}', response_model=Topic, responses=view_topic_by_id_response) 
def view_topic(
    id: Annotated[int, Path(description='The ID of the topic you want to view')]
    ) -> Topic or NotFound:

    '''Responds with a single Topic resource and a list of Reply resources'''

    topic = ts.get_topic_by_id(id)
    return topic if topic else NotFound(content=f'Topic with id {id} is not found')


@topics_router.post('/', status_code=status.HTTP_201_CREATED, responses=create_topic_response)
async def create_topic(
    title: str,
    text: str,
    category_id: int,
    token: Annotated[str, Depends(oauth2_scheme)]
    ) -> Topic or BadRequest:
    ''' requires authentication token '''

    user = await get_current_user(token)
    new_topic = Topic(
        title=title, 
        created_on=datetime.utcnow(),
        text=text, 
        category_id=category_id, 
        author_id=user.id
    )
    if ts.user_has_write_access(new_topic, user):
        try:
            ts.create_topic(new_topic)
        except mdb.IntegrityError as ie:
            return BadRequest(content=str(ie))
    
        return new_topic
    
    return Response(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content='User has no write access to that category!'
                    )

    
@topics_router.patch('/{id}', status_code=status.HTTP_201_CREATED, responses=edit_topic_response)
async def edit_topic(
        id: Annotated[int, Path(description='The ID of the topic you want to edit')],
        token: Annotated[str, Depends(oauth2_scheme)],
        new_title: Annotated[str | None, 
                             Query(min_length=2, 
                                   max_length=200, 
                                   description='Edit title between [2 | 200] symbols')] = None, 
        new_text: Annotated[str | None, 
                            Query(min_length=10, 
                                  max_length=1000, 
                                  description='Edit text between [10 | 1000] symbols')] = None
        ) -> Topic or NotFound: 
    
    '''the author (should be logged in/authenticated) 
        should be able to edit the name and/or content of the topic 
        What about admins? Maybe they can also edit other users's topics/replies'''
    user = await get_current_user(token)
    existing_topic = ts.get_topic_by_id(id=id)
    if not existing_topic:
        return NotFound
    
    if existing_topic.author_id != user.id and not user.is_admin:
        return Response(status_code=status.HTTP_403_FORBIDDEN, 
                        content='You are not the author of this topic!')
    
    if existing_topic.is_locked:
        return Locked(content='The topic is locked and cannot be modified!')

    return ts.edit_topic(existing_topic, new_title, new_text)
    
    
@topics_router.put('/{id}', status_code=status.HTTP_200_OK, responses=lock_topic_response) 
async def lock_topic(
        id: Annotated[int, Path(description='The ID of the topic you want to lock')],
        token: Annotated[str, Depends(oauth2_scheme)]
        ) -> Topic or NotFound:
    
    '''admin endpoint, the topic can no longer accept replies'''
    user = await get_current_user(token)
    existing_topic = ts.get_topic_by_id(id=id)
    
    if not existing_topic: return NotFound
    
    if not user.is_admin:
        return Response(
                        status_code=status.HTTP_403_FORBIDDEN, 
                        content='You are not admin!'
                        )    
    lock_result = ts.lock_topic(existing_topic.id)
    if not lock_result:
        return Response(
                        status_code=status.HTTP_208_ALREADY_REPORTED, 
                        content=f'Topic {existing_topic.id} already locked'
                        )
    existing_topic.is_locked = True
    return existing_topic
