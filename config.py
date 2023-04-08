# config.py

from pydantic import BaseSettings


class Settings(BaseSettings):
    NAVER_AUTH_URL: str = "https://nid.naver.com"
    NAVER_CLIENT_ID: str = "AGAJnqzf86FbR9Lfyv7H"
    NAVER_CLIENT_SECRET: str = ""


settings = Settings()
