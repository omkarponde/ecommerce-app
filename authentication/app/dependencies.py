from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from app.db import Session
from app.models import User
from app.exceptions import PermissionDeniedException, InvalidTokenException


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


def get_current_user(Authorize: AuthJWT = Depends(), session: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise InvalidTokenException()

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.id == current_user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def can_post_product(user: User = Depends(get_current_user)):
    if user.role not in ["admin", "seller"]:
        raise PermissionDeniedException()
    return user


def can_order_product(user: User = Depends(get_current_user)):
    if user.role not in ["admin", "buyer"]:
        raise PermissionDeniedException()
    return user
