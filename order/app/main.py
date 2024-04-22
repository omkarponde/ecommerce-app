from fastapi import FastAPI
from app.config import settings
from app.routes import order_router

app = FastAPI(title=settings.PROJECT_NAME, root_path=settings.API_PREFIX)

app.include_router(order_router)
