from fastapi import APIRouter, Depends, HTTPException, Header, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
import services.users_services as users_services
from typing import Annotated
import common.auth as auth
import common.responses as responses
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


users_router = APIRouter(prefix='/users')

templates = Jinja2Templates(directory="templates")


@users_router.post('/', response_model = auth.Token, status_code= status.HTTP_201_CREATED, responses={400: {"detail": "string"}})
async def register_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    '''
    parameters: Oauth2 form data - username, password
    act: - check whether username does not exist already, 
         - check whether password conforms to requirements: min. 8 symbols, 1 lowercase latin letter,
           1 upper case latin letter, 1 special character from [=+#?!@$%^&*-]
    output: upon unique username and conforming password - register user and log in (provide access and refresh token)
    possible responses (excl. pydantic validation error): 201 Created, 400 Bad Request - 
                        when either username not unique("The username provided does not exist")
                        or password non_conforming ("Password must be at leat 8 characters long, contain 
                        upper- and lower-case latin letters, digits and at least one of the special characters #?!@$%^&*-=+")
    '''
    registration = users_services.register(form_data.username, form_data.password)
    if isinstance(registration, AssertionError):
        raise HTTPException(status_code=responses.BadRequest().status_code, detail= f"{registration}")
    if not registration:
        raise HTTPException(status_code=responses.BadRequest().status_code, detail= "Username already exists") 
    username, password = registration
    user = auth.authenticate_user(username, password)
    tokens = auth.token_response(user)
    response = RedirectResponse(url="users/dashboard")
    response.set_cookie(key="access_token", value=tokens["access_token"], httponly=True, max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    response.set_cookie(key="refresh_token", value=tokens["refresh_token"], httponly=True, max_age=auth.REFRESH_TOKEN_EXPIRE_MINUTES)
    return response
     

@users_router.post("/token", response_model=auth.Token, responses={401: {"detail": "string"}})
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    '''
    parameters: Oauth2 form data - username, password
    act: - check whether username & password match to a registered user
    output: if matching user return JWT access token and JWT refresh token
    possible responses (excl. pydantic validation error): 200 OK, 
                        401 Unauthorized ("Incorrect username or password") - when no matching user
    '''
    # if... guest...
    # else:
    
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        response = RedirectResponse(url="users/dashboard")
        response.set_cookie(key="access_token", value="guest", httponly=True, max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        return response    
    tokens = auth.token_response(user)
    if user.is_admin == 1:
        response = RedirectResponse(url="users/dashboard/admin")
    else: 
        response = RedirectResponse(url="users/dashboard")
    response.set_cookie(key="access_token", value=tokens["access_token"], httponly=True, max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    response.set_cookie(key="refresh_token", value=tokens["refresh_token"], httponly=True, max_age=auth.REFRESH_TOKEN_EXPIRE_MINUTES)
    return response


@users_router.post("/token/refresh", response_model=auth.Token, responses={401: {"detail": "string"}})
async def refresh_token(access_token: str = Header(), refresh_token: str = Header()):
    '''
    parameters: JWT access token - header, JWT refresh token - header
    act: - check whether JWT refresh token is valid and matching JWT access token
    output: if matching provide new JWT access token and new JWT refresh token
    possible responses (excl. pydantic validation error): 200 OK, 
                        401 Unauthorized ("Could not validate credentials") -
                        when invalid refresh token or not matching tokens)
    '''
    user =  await auth.refresh_access_token(access_token, refresh_token)
    return auth.token_response(user)

@users_router.put("/admin", response_model = int, responses={400: {"detail": "string"}, 401: {"detail": "string"}})
async def get_user(request: Request, to_change:dict):
    '''
    parameters: JWT access token as Ouath2 authorization header, username in a dict {"username": "xyz"} in the body
                of user to be set as admin
    act: - check whether JWT acces token is valid and identify user as an admin, identify user to be set as admin
    output: change user to admin
    possible responses (excl. pydantic validation error): 200 OK (return eith 0 (user is already admin) or 
                        1 (user was set as admin)), 
                        401 Unauthorized ("Could not validate credentials") -
                        when invalid access token or not matching tokens
                        401 Unauthorized ("Not authorized to set admin priviliges") -
                        when identified user is not admin
                        400 Bad Request ("The username provided does not exist") - 
                        if username of user to be set as admin could not be found 
    '''
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    if access_token == "guest"....
    try:
        user: User = await auth.get_current_user(access_token) 
    except:
        us
    response.set_cookie(key="access_token", value=tokens["access_token"], httponly=True, max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    response.set_cookie(key="refresh_token", value=tokens["refresh_token"], httponly=True, max_age=auth.REFRESH_TOKEN_EXPIRE_MINUTES)   
    if user.is_admin == 0:
        raise HTTPException(status_code=responses.Unauthorized().status_code, detail= "Not authorized to set admin priviliges")
    update_user = auth.find_user(to_change.get("username"))
    if not update_user:
        raise HTTPException(status_code=responses.BadRequest().status_code, detail= "The username provided does not exist")
    return users_services.set_admin(update_user.id)
    
        


    


