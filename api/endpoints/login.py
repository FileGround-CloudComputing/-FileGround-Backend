from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
router = APIRouter()

origins = [
    "http://localhost",
    "*"
]

# JWT 설정
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/auth")
async def auth(code: str, state: str):
    # 네이버 액세스 토큰 발급 요청
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"
    redirect_uri = "YOUR_REDIRECT_URI"
    access_token_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}&state={state}"
    headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    response = requests.post(access_token_url, headers=headers)
    response.raise_for_status()
    access_token = response.json()["access_token"]

    # 네이버 유저 정보 요청
    user_api_url = "https://openapi.naver.com/v1/nid/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(user_api_url, headers=headers)
    response.raise_for_status()
    naver_id = response.json()["response"]["id"]
    nickname = response.json()["response"]["nickname"]

    # 네이버 ID를 사용하여 JWT 토큰 발급
    access_token_expires = datetime.utcnow(
    ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_payload = {"sub": naver_id, "exp": access_token_expires}
    access_token = jwt.encode(access_token_payload,
                              SECRET_KEY, algorithm=ALGORITHM)

    # JWT 토큰 반환
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup")
async def signup(nickname: str, password: str, access_token: str = Depends(oauth2_scheme)):
    # JWT 토큰 검증
    try:
        access_token_payload = jwt.decode(
            access_token, SECRET_KEY, algorithms=[ALGORITHM])
        naver_id = access_token_payload["sub"]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    # TODO: 회원가입 로직 구현
    # nickname과 password를 사용하여 사용자 계정 생성
    # 생성된 계정 정보를 데이터베이스에 저장

    return {"message": "User signed up successfully"}
