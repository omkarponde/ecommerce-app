from typing import Optional, Dict, Any, Union
from pydantic import BaseSettings, validator, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "Order Service"
    API_PREFIX: str = "/api/v1/order"
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    STRIPE_KEY: str = "sk_test_51P861uSFm6Yw92EQDZkhoH155XtrbQbSv09FDKcPTaj0oJx1roA3Qzw58NRqJzkhWd4lyQxzblUjimFJh8XfIShU00CDq9i8eY"

    SQLALCHEMY_DATABASE_URI: Union[Optional[PostgresDsn], Optional[str]] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True, always=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if v:
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            port=values.get("POSTGRES_PORT")
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
