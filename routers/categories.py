from fastapi import (
    APIRouter,
    Query,
    status,
    HTTPException,
    Request,
    Path,
    Form,
)
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Optional
from pydantic import StringConstraints
import services.categories_services as categories_services
from models.categories import CategoryResponseModel, Category
from models.topic import Topic
from models.user import User
import common.auth as auth
import common.responses as responses
from fastapi.templating import Jinja2Templates

categories_router = APIRouter(prefix="/categories")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory="templates/category_templates")


@categories_router.get("/", response_model=list[CategoryResponseModel])
async def view_categories(
    request: Request,
    name: Annotated[str | None, Query(max_length=45)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
):
    token = request.cookies.get("access_token")
    try:
        user = await auth.get_current_user(token)
        categories = categories_services.get_all_categories(user, name, page)
        return templates.TemplateResponse(
            "view_categories.html", {"request": request, "categories": categories}
        )
    except:
        categories = categories_services.get_all_categories(name_filter=name, page=page)
        return templates.TemplateResponse(
            "view_categories.html", {"request": request, "categories": categories}
        )


@categories_router.get("/create_category", response_class=HTMLResponse)
async def get_create_category_form(request: Request):
    return templates.TemplateResponse("create_category_form.html", {"request": request})

@categories_router.get("/set_category_privacy", response_class=HTMLResponse)
async def set_category_privacy(request: Request):
    return templates.TemplateResponse("set_privacy_form.html", {"request": request})

@categories_router.get("/set_read_write_access", response_class=HTMLResponse)
async def set_category_privacy(request: Request):
    return templates.TemplateResponse("set_read_write_access.html", {"request": request})

@categories_router.get("/view_privileged_users", response_class=HTMLResponse)
async def view_privileged_users(request: Request):
    return templates.TemplateResponse("view_privileged_users.html", {"request": request})

@categories_router.get("/revoke_user_access", response_class=HTMLResponse)
async def set_category_privacy(request: Request):
    return templates.TemplateResponse("revoke_user_access.html", {"request": request})

@categories_router.get("/lock_category", response_class=HTMLResponse)
async def get_create_category_form(request: Request):
    return templates.TemplateResponse("lock_category_form.html", {"request": request})

@categories_router.get("/{cat_id}", response_model=list[Topic])
async def view_topics_by_category_id(
    cat_id: Annotated[int, Path(ge=1)],
    request: Request,
    topic_title: Annotated[str, StringConstraints(min_length=1, max_length=200)] = None,
    sorted: Annotated[str, StringConstraints(pattern="^(asc|desc)$")] = "asc",
    page: Annotated[int, Query] = 1,
):
    token = request.cookies.get("access_token")
    try:
        user = await auth.get_current_user(token)
        topics = categories_services.get_topics_by_cat_id(
            cat_id=cat_id, user=user, title=topic_title, sorting=sorted, page=page
        )
        return templates.TemplateResponse(
            "view_topics_by_cat.html", {"request": request, "topics": topics}
        )
    except:
        topics = categories_services.get_topics_by_cat_id(
            cat_id=cat_id, title=topic_title, sorting=sorted, page=page
        )
        return templates.TemplateResponse(
            "view_topics_by_cat.html", {"request": request, "topics": topics}
        )


@categories_router.get("/{cat_id}/privileged_users")
async def get_privileged_users_by_cat(
    cat_id: Annotated[int, Path(ge=1)],
    request: Request,
):
    token = request.cookies.get("access_token")
    logged_user: User = await auth.get_current_user(token)
    if logged_user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="You are not admin! You are not authorized to see privileged_users!",
        )

    try:
        privileged_users = categories_services.get_privileged_users(cat_id)
        return templates.TemplateResponse("return_view_privileged_users.html", {"request": request, "privileged_users": privileged_users})
    except:
        return templates.TemplateResponse("return_vpu_no_cont.html", {"request": request, "content": f"Category with id '{cat_id}' is not private or it doesn't exists!"})
    


@categories_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    request: Request,
    name: str = Form(min_length=1, max_length=45),
    privacy_status: str = Form(pattern="^(private|non_private)$"),
    access_status: str = Form(pattern="^(locked|unlocked)$"),
):
    token = request.cookies.get("access_token")
    user: User = await auth.get_current_user(token)
    if user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="Not authorized to create Category!",
        )

    category = Category(
        name=name,
        privacy_status=privacy_status,
        access_status=access_status,
    )
    
    try:
        category = categories_services.create_new_category(category, user.id)
        return templates.TemplateResponse("return_category_model.html", {"request": request, "category": category})
    except:
        return templates.TemplateResponse("return_category_duplicate.html", {"request": request, "content": f"Category with name '{category.name}' already exists!"})

@categories_router.post("/{cat_id}")
async def lock_category(
    request: Request,
    cat_id: Annotated[int, Path(ge=1)]
):
    token = request.cookies.get("access_token")
    logged_user: User = await auth.get_current_user(token)
    if logged_user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="You are not admin! You are not authorized to lock categories!",
        )

    try:
        categories_services.lock_category_by_id(cat_id)
    except:
        return templates.TemplateResponse("return_lock_category.html", {"request": request, "content": f"Category with id '{cat_id}' doesnt exists or it's already locked!"})

    return templates.TemplateResponse("return_lock_category.html", {"request": request, "content": f"Category '{cat_id}' was locked."})

@categories_router.post("/{cat_id}/privacy", status_code=status.HTTP_200_OK)
async def change_privacy(
    request: Request,
    cat_id: Annotated[int, Path(ge=1)],
    privacy_status: str = Form(pattern="^(private|non_private)$"),
):
    token = request.cookies.get("access_token")
    user: User = await auth.get_current_user(token)
    if user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="Not authorized to change the category status!",
        )

    try:
        response = categories_services.change_category_privacy(cat_id, privacy_status)
    except:
        return templates.TemplateResponse(
            "return_change_privacy.html",
            {
                "request": request,
                "content": f"Category with id '{cat_id}' doesnt exist or it's status is already {privacy_status}!",
            },
        )
    return templates.TemplateResponse(
        "return_change_privacy.html",
        {
            "request": request,
            "content": f"Category '{cat_id}' changed status to '{privacy_status}'.",
        },
    )


@categories_router.post("/{cat_id}/access", status_code=status.HTTP_200_OK)
async def revoke_user_access(
    request: Request,
    cat_id: Annotated[int, Path(ge=1)],
    user_id: int = Form(ge=1),
):
    token = request.cookies.get("access_token")
    logged_user: User = await auth.get_current_user(token)
    if logged_user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="You are not admin! You are not authorized to revoke user access!",
        )

    categories_services.revoke_access(user_id, cat_id)
    
    return templates.TemplateResponse("return_revoke_access.html", {"request": request, "content": f"If a user with the ID '{user_id}' previously had access to the category with ID '{cat_id}', they have already lost that access."})


@categories_router.post("/{cat_id}/access/read", status_code=status.HTTP_200_OK)
async def give_user_read_access(
    request: Request,
    cat_id: Annotated[int, Path(ge=1)],
    user_id: int = Form(ge=1),
):
    token = request.cookies.get("access_token")
    logged_user: User = await auth.get_current_user(token)
    if logged_user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="You are not admin! You are not authorized to give read access!",
        )
    try:
        categories_services.give_read_access_to_user(user_id, cat_id)
    except:
        return templates.TemplateResponse(
            "return_crws_form.html",
            {
                "request": request,
                "content": f"Category with id '{cat_id}' is not private, user with id '{user_id}' is not valid user or he already has this access!",
            },
        )

    return templates.TemplateResponse(
        "return_crws_form.html",
        {
            "request": request,
            "content": f"'User '{user_id}' can now only read topics in category '{cat_id}'.",
        },
    )


@categories_router.post("/{cat_id}/access/write", status_code=status.HTTP_200_OK)
async def give_user_write_access(
    request: Request,
    cat_id: Annotated[int, Path(ge=1)],
    user_id: int = Form(ge=1),
):
    token = request.cookies.get("access_token")
    logged_user: User = await auth.get_current_user(token)
    if logged_user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="You are not admin! You are not authorized to give write access!",
        )

    try:
        categories_services.give_write_access_to_user(user_id, cat_id)
    except:
        return templates.TemplateResponse(
            "return_crws_form.html",
            {
                "request": request,
                "content": f"Category with id '{cat_id}' is not private, user with id '{user_id}' is not valid user or he already has this access!",
            },
        )

    return templates.TemplateResponse(
        "return_crws_form.html",
        {
            "request": request,
            "content": f"'User '{user_id}' can now write topics in category '{cat_id}'.",
        },
    )


