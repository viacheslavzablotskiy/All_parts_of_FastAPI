from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.db.database import metadata
from src.db.base_class import Base


class User(Base):
    """Model user"""
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    post = relationship("Post", back_populates="user")


class Post(Base):
    """Model post"""
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    slug = Column(String, unique=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User, back_populates="post")


operation = Table(
    "operations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("name", String),
)
