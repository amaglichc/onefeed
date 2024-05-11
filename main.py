from fastapi import FastAPI

from Auth.AuthRouter import router as auth_router
from routers.CommentRouter import router as comment_router
from routers.PostsRouter import router as post_router
from routers.UserRouter import router as user_router

app = FastAPI(
    title="OneFeed"
)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)
app.include_router(comment_router)
