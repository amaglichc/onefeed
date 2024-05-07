from fastapi import FastAPI

from routers.PostsRouter import router as post_router
from routers.UserRouter import router as user_router
from Auth.AuthRouter import router as auth_router
app = FastAPI(
    title="OneFeed"
)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)
