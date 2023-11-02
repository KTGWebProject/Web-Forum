from fastapi import APIRouter, Depends, Query, status, HTTPException, Request, Path
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import StringConstraints, Field
import services.categories_services as categories_services
from models.categories import CategoryResponseModel, Category
from models.topic import Topic
from models.user import User
import common.auth as auth
import common.responses as responses
from fastapi.templating import Jinja2Templates

categories_router = APIRouter(prefix="/categories")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory="templates")

@categories_router.get(
    "/", response_model=list[CategoryResponseModel]
)
async def view_categories(
    request: Request,
    name: Annotated[str | None, Query(max_length=45)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
): 
    token = request.cookies.get("access_token")
    try:
        user = await auth.get_current_user(token)
        categories = categories_services.get_all_categories(user, name, page)
        return templates.TemplateResponse("view_categories.html", {"request": request, "categories": categories})
    except:
        categories = categories_services.get_all_categories(name_filter=name, page=page)
        return templates.TemplateResponse("view_categories.html", {"request": request, "categories": categories})

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
        return templates.TemplateResponse("view_topics_by_cat.html", {"request": request, "topics": topics})
    except:
        topics = categories_services.get_topics_by_cat_id(
            cat_id=cat_id, title=topic_title, sorting=sorted, page=page
        )
        return templates.TemplateResponse("view_topics_by_cat.html", {"request": request, "topics": topics})

@categories_router.get("/{cat_id}/privileged_users")
async def get_privileged_users_by_cat(
    cat_id: Annotated[int, Path(ge=1)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    logged_user: User = await auth.get_current_user(token)
    if logged_user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="You are not admin! You are not authorized to see privileged_users!",
        )

    return categories_services.get_privileged_users(cat_id)


@categories_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(cat: Category, token: Annotated[str, Depends(oauth2_scheme)]):
    user: User = await auth.get_current_user(token)
    if user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="Not authorized to create Category!",
        )

    category = Category(
        name=cat.name,
        privacy_status=cat.privacy_status,
        access_status=cat.access_status,
    )
    return categories_services.create_new_category(category, user.id)


@categories_router.put("/{cat_id}/privacy", status_code=status.HTTP_200_OK)
async def change_privacy(
    cat_id: Annotated[int, Path(ge=1)],
    privacy_status: Annotated[
        str, StringConstraints(pattern="^(private|non_private)$")
    ],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    user: User = await auth.get_current_user(token)
    if user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="Not authorized to change the category status!",
        )

    return categories_services.change_category_privacy(cat_id, privacy_status)


@categories_router.put("/{cat_id}/access/read", status_code=status.HTTP_200_OK)
async def give_user_read_access(
    cat_id: Annotated[int, Path(ge=1)],
    user_id: Annotated[int, Query(ge=1)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    logged_user: User = await auth.get_current_user(token)
    if logged_user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="You are not admin! You are not authorized to give read access!",
        )

    return categories_services.give_read_access_to_user(user_id, cat_id)


@categories_router.put("/{cat_id}/access/write", status_code=status.HTTP_200_OK)
async def give_user_write_access(
    cat_id: Annotated[int, Path(ge=1)],
    user_id: Annotated[int, Query(ge=1)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    logged_user: User = await auth.get_current_user(token)
    if logged_user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="You are not admin! You are not authorized to give write access!",
        )

    return categories_services.give_write_access_to_user(user_id, cat_id)


@categories_router.patch("/{cat_id}")
async def lock_category(
    cat_id: Annotated[int, Path(ge=1)], token: Annotated[str, Depends(oauth2_scheme)]
):
    logged_user: User = await auth.get_current_user(token)
    if logged_user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="You are not admin! You are not authorized to lock categories!",
        )

    return categories_services.lock_category_by_id(cat_id)


@categories_router.delete("/{cat_id}/access", status_code=status.HTTP_200_OK)
async def revoke_user_access(
    cat_id: Annotated[int, Path(ge=1)],
    user_id: Annotated[int, Query(ge=1)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    logged_user: User = await auth.get_current_user(token)
    if logged_user.is_admin == 0:
        raise HTTPException(
            status_code=responses.Unauthorized().status_code,
            detail="You are not admin! You are not authorized to revoke user access!",
        )

    return categories_services.revoke_access(user_id, cat_id)
