from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.posts.schemas import PostCreate, PostList, PostSingle
from src.auth.security import get_current_user
from src.auth.models import User as DBUser
from src.posts.create_post import create_post, get_post_single, get_posts, get_current_user_posts
from src.db.database import get_db

router = APIRouter()


@router.post("/post/", response_model=PostCreate)
def create_posts(item: PostCreate, db: Session = Depends(get_db),
                 current_user: DBUser = Depends(get_current_user)):
    current_user_json = jsonable_encoder(current_user)
    current_user_json = current_user_json.get('id')
    return create_post(db=db, item=item, user_id=current_user_json)


@router.get('/posts_list_for_current_user', response_model=List[PostList])
def get_all_posts_for_current_user(db: Session = Depends(get_db),
                                   current_user: DBUser = Depends(get_current_user)):
    current_user_json = jsonable_encoder(current_user)
    get_current_user_json = current_user_json.get('id')
    return get_current_user_posts(db=db, user_id=get_current_user_json)


@router.get("/post/", response_model=List[PostList])
def get_post_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_posts(db=db, skip=skip, limit=limit)


@router.get("/post/{post_id}", response_model=PostSingle)
def get_post_detail(post_id: int, db: Session = Depends(get_db)):
    return get_post_single(db=db, post_id=post_id)
