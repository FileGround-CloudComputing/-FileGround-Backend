import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    PROJECT_NAME: str = 'FileGround'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []


settings = Settings()
