from fastapi import APIRouter, status, Depends
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.exceptions import HTTPException
from app.schemas import SignUpModel, LoginModel, UserResponseModel
from app.models import User
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

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        role=user.role,
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

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response = {
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid Username Or Password"
                        )


@auth_router.get('/refresh')
def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please provide a valid refresh token"
                            )

    current_user = Authorize.get_jwt_subject()

    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access": access_token})
