from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.posts.schemas import PostCreate
from src.auth.models import Post


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Post).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_current_user_posts(db: AsyncSession, user_id: int):
    query = select(Post).where(Post.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()



async def get_post_single(db: AsyncSession, post_id: int):
    query = select(Post).where(Post.id == post_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_post(db: AsyncSession, item: PostCreate, user_id: int):
    count_id = select(Post)
    count_id_1 = await db.execute(count_id)
    len_list = len(count_id_1.scalars().all())
    item_main = PostCreate(id=len_list+1, title=item.title, slug=item.slug, user_id=user_id, description=item.description)
    db_item = insert(Post).values(**item_main.dict())
    # db_item = Post(
    #     title=item.title,
    #     slug=item.slug,
    #     user_id=user_id,
    #     description=item.description
    # )
    await db.execute(db_item)
    await db.commit()

    result = select(Post).where(Post.id == len_list - 1)
    result_1 = await db.execute(result)

    return result_1.scalars().first()