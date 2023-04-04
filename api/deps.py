from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

import models
from core import security

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"")

# def get_db() -> Generator:
#     try:
#         db = Session


def get_current_user(
    db: Session = Depends(), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[security.ALGORITHM])

    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="유효하지 않은 검증입니다")
    return null
