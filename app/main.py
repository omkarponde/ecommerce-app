from fastapi import FastAPI
from app.routes import user_router, product_router, order_router, auth_router
from app.schemas import Settings
from fastapi_jwt_auth import AuthJWT

app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(auth_router)

@AuthJWT.load_config
def get_config():
    return Settings()
