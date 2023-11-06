from datetime import datetime
from pydantic import constr
from fastapi import APIRouter, Depends, Query, Body, status, Request, HTTPException, Form
from typing import Annotated, Optional
from common import auth
from services.messages_services import get_messages, get_messages_user, post_message, flatten
from models.user import User
from common import responses
from models.message import Message, MessageResponseModelConversation, MessageResponseModelChat
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates



messages_router = APIRouter(prefix='/messages')
templates = Jinja2Templates(directory="templates")



@messages_router.post('/',name="send_message", response_model=int, status_code=status.HTTP_201_CREATED, responses={401: {"detail": "string"}})
async def send_message(
    request: Request,
    id_parent_message:str = Form(None),
    recipients: str = Form(...),
    subject: str = Form(...),
    content:str = Form(...)
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
    access_token = request.cookies.get("access_token")
    user: User = await auth.get_current_user(access_token)
    try:
        await post_message(user.id, recipients, subject, content, id_parent_message)
    except:
        return templates.TemplateResponse("no_such_user_template.html", context={"request": request})
    return templates.TemplateResponse("message_sent.html", context={"request": request})
        
    
@messages_router.get("/template")
async def get_sendtemplate(request: Request, old_content: str = Query(""), 
                           id_parent_message:int = Query(None),
                           previous_author: str= Query(""),
                           previous_subject: str = Query("")):
    access_token = request.cookies.get("access_token")
    if access_token == auth.DUMMY_ACCESS_TOKEN:
        response = RedirectResponse(url="/users/dashboard", status_code=303)
    else:
        try:
            await auth.get_current_user(access_token)
            response = templates.TemplateResponse("send_message_template.html", context={"request": request, "old_content": old_content, "id_parent_message": id_parent_message, "previous_author": previous_author, "previous_subject": previous_subject})
        except:   
            response = RedirectResponse(url="/", status_code=303)
    return response       

@messages_router.get("/")
async def get_all_user(request: Request, users: str = Query(""), paginated: str = Query(None), sort: str = Query(None), page: str = Query(1)):
    access_token = request.cookies.get("access_token")
    
    if not paginated:
        paginated = False
    else:
        paginated = True
    
    if not sort:
        sort = True
    else:
        sort = False
    if page:
        page_int = int(page)
    if access_token == auth.DUMMY_ACCESS_TOKEN:
        response = RedirectResponse(url="/users/dashboard", status_code=303)
    else:
        try:
            user = await auth.get_current_user(access_token)
            if users == "":
                if not page:
                    messages = await get_messages(user.id, sort, paginated, page=1)
                else:
                    messages = await get_messages(user.id, sort, paginated, page_int)
            else:
                users_lst=users.split(", ")
                final_query_params = {}
                counter = 1
                for counterparty in users_lst:
                    final_query_params["username"+str(counter)] = counterparty
                    counter += 1
                messages = await get_messages_user(user_id = user.id, sort=sort, paginated=paginated, page=page, **final_query_params)
            check_not_empty = flatten(messages)
            if len(check_not_empty)==0:
                not_empty=False
            else:
                not_empty= True
            response = templates.TemplateResponse("view_messages.html", context={"request": request, "messages": messages, "main_user": user.username, "sort":sort, "paginated":paginated, "page":page_int, "empty":not_empty, "users":users})
        except Exception as exc:   
            response = RedirectResponse(url="/", status_code=303)
    return response         

@messages_router.get("/viewtemplate")
async def get_viewtemplate(request: Request):
    access_token = request.cookies.get("access_token")
    if access_token == auth.DUMMY_ACCESS_TOKEN:
        response = RedirectResponse(url="/users/dashboard", status_code=303)
    else:
        try:
            await auth.get_current_user(access_token)
            response = templates.TemplateResponse("get_messages_template.html", context={"request": request})
        except:   
            response = RedirectResponse(url="/", status_code=303)
    return response   
    