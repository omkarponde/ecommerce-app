from fastapi import APIRouter, status, Depends
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.exceptions import HTTPException
from app.schemas import SignUpModel, LoginModel, UserResponseModel
from app.models import User, Role
from app.db import Session
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from app.dependencies import get_current_user, get_db
from app.exceptions import InvalidTokenException, EmailAlreadyExists, UsernameAlreadyExists

auth_router = APIRouter(
    prefix='',
    # tags=['auth']
)


@auth_router.get('/ping', status_code=status.HTTP_204_NO_CONTENT)
async def ping():
    pass


@auth_router.post('/signup', response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
def create_user(user: SignUpModel, session: Session = Depends(get_db)):
    existing_username = session.query(User).filter(User.username == user.username).first()
    existing_email = session.query(User).filter(User.email == user.email).first()

    if existing_username is not None:
        raise UsernameAlreadyExists()

    if existing_email is not None:
        raise EmailAlreadyExists()

    user_role = session.query(Role).filter(Role.name == user.role).first()
    print(user_role.id)

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=generate_password_hash(user.password),
        role_id=user_role.id,
        is_active=user.is_active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@auth_router.post('/login', status_code=status.HTTP_200_OK)
def login(
        user: LoginModel,
        Authorize: AuthJWT = Depends(),
        session: Session = Depends(get_db)
):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password_hash, user.password):
        access_token = Authorize.create_access_token(subject=db_user.id)
        refresh_token = Authorize.create_refresh_token(subject=db_user.id)

        response = {
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid Username Or Password"
                        )


@auth_router.get('/validate')
def permissions(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    user_role = session.query(Role).filter(Role.id == current_user.role_id).first()
    return {
        "user_id": current_user.id,
        "role": user_role.name
    }


@auth_router.get('/user-profile', response_model=UserResponseModel, status_code=status.HTTP_200_OK)
def user_profile(current_user: User = Depends(get_current_user)):
    return current_user

