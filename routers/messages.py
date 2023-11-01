from datetime import datetime
from pydantic import constr
from fastapi import APIRouter, Depends, Query, Body, status, Request, HTTPException
from typing import Annotated, Optional
from common import auth
from services.messages_services import get_messages, get_messages_user, post_message, get_chat_service
from models.user import User
from common import responses
from models.message import Message, MessageResponseModelConversation, MessageResponseModelChat
from fastapi.responses import JSONResponse




messages_router = APIRouter(prefix='/messages')


@messages_router.get('/', response_model=list[list[MessageResponseModelConversation]], responses={401: {"detail": "string"}})
async def get_conversations(
    token: Annotated[str, Depends(auth.oauth2_scheme)],
    sort: bool = Query(True),
    paginated: bool = Query(False), 
    page: int = Query(1)
):
    '''
    parameters: JWT access token as Ouath2 authorization ,sort = Query(True), paginated = Query(False), page = Query(1)
    act: - check whether JWT acces token is valid and identify user
    output: provide a list of all messages that the user has exchanged with any other user - 
            for each user with whom messages were exchanged the output is a list of messages
    possible responses (excl. pydantic validation error): 200 OK (list[list[MessageResponseModelConversation]] - 
                        could be [] if no messages), 
                        401 Unauthorized ("Could not validate credentials") -
                        when invalid access token)
    '''
    user: User = await auth.get_current_user(token)
    return await get_messages(user.id, sort, paginated, page)


@messages_router.get('/specified', response_model=list[list[list[MessageResponseModelConversation]]], responses={401: {"detail": "string"}})
async def get_conversations_users(
    token: Annotated[str, Depends(auth.oauth2_scheme)],
    request: Request,
    sort: bool = Query(True),
    paginated: bool = Query(False), 
    page: int = Query(1)
    
):
    '''
    parameters: JWT access token as Ouath2 authorization, 
                besides sort = Query(True), paginated = Query(False), page = Query(1), 
                Request (Query) should include usernames of users with whom messages were exchanged. If more than
                1 username is specified key for each username should be different. 
    act: - check whether JWT acces token is valid and identify user 
    output: provide a list of all messages that the user has exchanged with the specified user(s) - 
            for each specified user with whom messages were exchanged the output is a list of messages, further split by
            sublists according to subject
            if no (correct) usernames are specified or no messages exchanged with specified usersnames, response - [[[]]]
    possible responses (excl. pydantic validation error): 200 OK (list[list[list[MessageResponseModelConversation]]];
                        could be [] if no messages with each username provided or if no usernames provided), 
                        401 Unauthorized ("Could not validate credentials") -
                        when invalid access token)
    '''
    query_params = dict(request.query_params)
    to_remove=["sort", "paginated", "page"]
    final_query_params = {key: value for key, value in query_params.items() if key not in to_remove}
    
    
    user: User = await auth.get_current_user(token)
    return await get_messages_user(user_id = user.id, sort=sort, paginated=paginated, page=page, **final_query_params)

@messages_router.get('/chat', response_model=list[MessageResponseModelChat], responses={401: {"detail": "string"}})
async def get_chat(
    token: Annotated[str, Depends(auth.oauth2_scheme)],
    since = Query(datetime)
):
    '''
    parameters: JWT access token as Ouath2 authorization, since = Query(datetime)
    act: - check whether JWT acces token is valid and identify user 
    output: provide all messages that the user has received from any other user from the point specified 
            in "since" parameter
    possible responses (excl. pydantic validation error): 200 OK (list[MessageResponseModelChat]] - 
                        could be [] if no messages), 
                        401 Unauthorized ("Could not validate credentials") -
                        when invalid access token)
    '''
    user: User = await auth.get_current_user(token)
    return await get_chat_service(user.id, since)

@messages_router.post('/', response_model=int, status_code=status.HTTP_201_CREATED, responses={401: {"detail": "string"}})
async def send_message(
    token: Annotated[str, Depends(auth.oauth2_scheme)],
    message: Annotated[Message, Body],
    recipients: Annotated[set[constr(min_length=1, max_length = 60)], Body]
    ):
    '''
    parameters: JWT access token as Ouath2 authorization, message: Annotated[Message, Body],
                recipients: Annotated[set[constr], Body],
                reply_to: Optional[int] = Body(None)) - id of message to which the message to be posted is a reply
    act: - check whether JWT acces token is valid and identify user 
    output: provide all messages that the user has received from any other user from the point specified 
            in "since" parameter
    possible responses (excl. pydantic validation error): 201 Created (id: int of message psoted), 
                        401 Unauthorized ("Could not validate credentials") -
                        when invalid access token)
    '''
    
    user: User = await auth.get_current_user(token)
    
    return await post_message(user.id, message, recipients)
    
    
    
    
    