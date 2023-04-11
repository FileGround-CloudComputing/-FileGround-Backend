# services.py

from typing import Dict

from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
from jose import jwt, JWTError
from datetime import datetime, timedelta

from config import settings
# from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/access")

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginService:
    def get_naver_login_url(self, redirect_uri: str) -> str:
        url = f"{settings.NAVER_AUTH_URL}/oauth2.0/authorize"
        params = {
            "response_type": "code",
            "client_id": settings.NAVER_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "state": "naver",
        }
        return f"{url}?{self._get_query_string(params)}"

    async def get_naver_login_token(self, code: str, state: str) -> str:
        url = f"{settings.NAVER_AUTH_URL}/oauth2.0/token"
        params = {
            "grant_type": "authorization_code",
            "client_id": settings.NAVER_CLIENT_ID,
            "client_secret": settings.NAVER_CLIENT_SECRET,
            "code": code,
            "state": state,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }
        response = await self._send_request(url, params, headers)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to get access token")
        return response.json()

    async def _send_request(self, url: str, params: Dict[str, str], headers: Dict[str, str]) -> requests.Response:
        response = requests.post(url, data=params, headers=headers)
        return response

    def _get_query_string(self, params: Dict[str, str]) -> str:
        query_string = ""
        for key, value in params.items():
            query_string += f"{key}={value}&"
        return query_string[:-1]


class TestLoginService:

    # 사용자 인증 함수
    def authenticate_user(username: str, password: str):
        user = get_user(username)
        if not user:
            return False
        if not verify_password(password, user["hashed_password"]):
            return False
        return user

    # JWT 토큰 생성 함수
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


login_service = LoginService()
test_login_service = TestLoginService()
