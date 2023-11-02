from fastapi import FastAPI, Request
from routers.topics import topics_router
from routers.replies import replies_router
from routers.users import users_router
from routers.categories import categories_router
from routers.messages import messages_router
from fastapi.templating import Jinja2Templates
import uvicorn
from common.auth import TokenValidationMiddleware

app = FastAPI()
app.include_router(topics_router)
app.include_router(replies_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(messages_router)
app.add_middleware(TokenValidationMiddleware)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def landing_page(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})    


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
