from fastapi import FastAPI

from app.config import settings
from app.routes import auth_router
from app.schemas import Settings
from fastapi_jwt_auth import AuthJWT

app = FastAPI(title=settings.PROJECT_NAME, root_path=settings.API_PREFIX)

app.include_router(auth_router)


@AuthJWT.load_config
def get_config():
    return Settings()
