from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.crud_user.service import CRUDBase
from src.auth.models import User
from src.auth.schemas import UserCreate, UserUpdate, UserCreate1, UserInDB
from src.utils import verify_password, get_password_hash



class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def get_by_email(self, db_session: AsyncSession, *, email: str) -> Optional[User]:
        result = select(User).where(User.email == email)
        query = await db_session.execute(result)
        return query.scalars().first()

    async def create(self, db_session: AsyncSession, *, obj_in: UserCreate1):
        # UserTnDB
        # obj_in.hashed_password = await get_password_hash(obj_in.hashed_password)
        all_user = select(User)
        all_user_1 = await db_session.execute(all_user)
        x = len(all_user_1.scalars().all())
        # user_in = UserInDB(hashed_password=
        # await get_password_hash(obj_in.password), email=obj_in.email, full_name=obj_in.full_name)
        obj_in = UserCreate1(id=x+1, full_name=obj_in.full_name,email=obj_in.email,
                             hashed_password=obj_in.hashed_password)
        db_obj = insert(User).values(**obj_in.dict())

        await db_session.execute(db_obj)
        await db_session.commit()
        obj_in_test = select(User).where(User.id == obj_in.id)
        obj_in_test_1 = await db_session.execute(obj_in_test)
        return obj_in_test_1.scalars().first()
        # else:
        #     user_in = UserInDB(id=1, hashed_password=
        #     await get_password_hash(obj_in.password), email=obj_in.email, full_name=obj_in.full_name)
        #     db_obj = insert(User).values(**user_in.dict())
        #
        #     await db_session.execute(db_obj)
        #     await db_session.commit()
        #     await db_session.refresh(db_obj)
        #     return db_obj

    async def authenticate(
            self, db_session: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(db_session, email=email)
        if not user:
            return None
        if not await verify_password(password, user.hashed_password):
            return None
        return user

    async def is_active(self, user: User) -> bool:
        return user.is_active

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser


crud_user = CRUDUser(User)
