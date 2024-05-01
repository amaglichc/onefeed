from fastapi import FastAPI

from routers.PostsRouter import router as post_router
from routers.UserRouter import router as user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)
