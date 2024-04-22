from fastapi import Header, status, Depends
import requests
from fastapi.exceptions import HTTPException
from app.exceptions import PermissionDeniedException
from app.db import Session


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


def is_user_authorized(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")

    try:
        token_type, token = authorization.split()
        if token_type.lower() != 'bearer':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")

    protected_endpoint = "http://authentication:8000/api/v1/authentication/validate"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(protected_endpoint, headers=headers)
    if response.status_code == status.HTTP_200_OK:
        user = response.json()
        if 'role' in user.keys():
            return user

        raise PermissionDeniedException()
    # print(response.json())
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=response.json().get('details', 'Invalid token'))


def can_buy_product(user: dict = Depends(is_user_authorized)):
    if user['role'] != "buyer":
        raise PermissionDeniedException()
    return user


