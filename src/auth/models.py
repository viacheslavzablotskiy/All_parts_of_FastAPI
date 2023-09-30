from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.db.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    post = relationship("Post", back_populates="user")



class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    slug = Column(String, unique=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User, back_populates="post")

# users = Table(
#     'user',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('full_name', String, index=True),
#     Column('email', String, unique=True, index=True),
#     Column('hashed_password', String),
#     Column('is_active', Boolean, default=True),
#     Column('is_superuser', Boolean, default=False),
# )
#
# posts = Table(
#     'post',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('title', String),
#     Column('description', String),
#     Column('slug', String, unique=True),
#     Column('user_id', Integer, ForeignKey('user.id')),
# )