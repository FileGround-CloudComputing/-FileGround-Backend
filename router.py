# views.py

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from services import login_service

router = APIRouter()


@router.get("/naver/login")
async def naver_login(request: Request):
    redirect_uri = request.url_for("naver_callback")
    print('redirect_uri:', redirect_uri)
    naver_login_url = login_service.get_naver_login_url(redirect_uri)
    return HTMLResponse(f'<h1><a href="{naver_login_url}">Sign in with Naver</a></h1>')


@router.get("/naver/callback")
async def naver_callback(request: Request, response: Response, code: str = None, state: str = None):
    if code is None or state is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Missing code or state parameter")
    login_token = await login_service.get_naver_login_token(code, state)
    response.set_cookie(key="access_token", value=login_token["access_token"])
    return login_token
    # return {"access_token": login_token["access_token"]}


@router.get("/auth/refresh")
async def auth_refresh(request: Request):
    return HTMLResponse()
