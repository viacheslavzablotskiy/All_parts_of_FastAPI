from fastapi import APIRouter

from src.api.endpoint import users, posts, users_router

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(users_router.router, tags=["login"])
