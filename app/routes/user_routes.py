from typing import List
from fastapi import APIRouter, status, Depends
from datetime import datetime
from app.models import User
from app.schemas import UpdateUserModel, UserResponseModel
from app.exceptions import UserNotFoundException
from app.db import Session
from app.dependencies import get_current_user, get_db

user_router = APIRouter(
    prefix='/users',
    tags=['user']
)


@user_router.get('', response_model=List[UserResponseModel], status_code=status.HTTP_200_OK)
async def get_all_users(session: Session = Depends(get_db)):
    users = session.query(User).all()
    return users


@user_router.get('/{user_id}', response_model=UserResponseModel, status_code=status.HTTP_200_OK)
async def get_user_by_id(
        user_id: int,
        session: Session = Depends(get_db)
):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UserNotFoundException(user_id)
    return user


@user_router.put("/", response_model=UserResponseModel, status_code=status.HTTP_200_OK)
def update_user(
        user_data: UpdateUserModel,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_db)
):
    #TODO: add email and username validation
    if user_data.username is not None:
        user.username = user_data.username
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.password is not None:
        user.password = user_data.password
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    user.updated_at = datetime.now()

    session.commit()
    session.refresh(user)

    return user

#Not Running properly, still has work to do, not a very important api so leaving it rn.
# deactivate
@user_router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user: User = Depends(get_current_user),
        session: Session = Depends(get_db)
):
    session.delete(user)
    session.commit()

    return {"message": "Successfully deleted"}
