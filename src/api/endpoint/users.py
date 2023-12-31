from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from src.auth.security import get_current_active_superuser, get_current_active_user


from src.db.database import get_db


from src.auth.models import User as DBUser
from src.auth.schemas import User, UserCreate, UserUpdate
from src.auth.utils import crud_user


router = APIRouter()


@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,

):
    """
    Retrieve users.
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,

):
    """
    Create new user.
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud_user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud_user.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=User)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=User)
def create_user_open(
    *,
    db: Session = Depends(get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
):
    """
    Create new user without the need to be logged in.
    """
    # if not USERS_OPEN_REGISTRATION:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Open user registration is forbidden on this server",
    #     )
    user = crud_user.get_by_email(db_session=db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = UserCreate(password=password, email=email, full_name=full_name)
    user = crud_user.create(db_session=db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=User)
def read_user_by_id(
    user_id: int,
    current_user: DBUser = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific user by id.
    """
    user = crud_user.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud_user.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: DBUser = Depends(get_current_active_superuser),
):
    """
    Update a user.
    """
    user = crud_user.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud_user.user.update(db, db_obj=user, obj_in=user_in)
    return user
