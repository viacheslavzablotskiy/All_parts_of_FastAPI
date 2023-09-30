from sqlalchemy.orm import Session
from src.posts.schemas import PostCreate
from src.auth.models import Post

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


def get_current_user_posts(db: Session, user_id: int):
    return db.query(Post).where(Post.user_id == user_id).all()


def get_post_single(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def create_post(db: Session, item: PostCreate, user_id: int):
    db_item = Post(
        title=item.title,
        slug=item.slug,
        user_id=user_id,
        description=item.description
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
