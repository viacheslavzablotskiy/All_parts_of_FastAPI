from pydantic import BaseModel


class PostBase(BaseModel):
    """Base model schemas post"""
    title: str
    slug: str
    user_id: int

    class Config:
        orm_mode = True


class PostList(PostBase):
    pass


class PostCreate(PostBase):
    description: str



class PostSingle(PostBase):
    description: str