import aioredis
from celery.backends.redis import RedisBackend
from fastapi import FastAPI
from sqladmin import Admin, ModelView

from src.auth.models import User, Post
from src.db.database import engine
from src.api.base_router import api_router as all_routers
from src.tasks.router import router as email_router

app = FastAPI()

admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.full_name, User.email, User.hashed_password, User.is_active, User.is_superuser]


class CreatePost(ModelView, model=Post):
    column_list = [Post.id, Post.title, Post.description, Post.slug, Post.user_id]


admin.add_view(UserAdmin)
admin.add_view(CreatePost)

app.include_router(all_routers)
app.include_router(email_router)


