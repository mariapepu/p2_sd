"""
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic.tools import lru_cache
from sqlalchemy.orm import Session


import repository
import utils
from jose import jwt
from pydantic import ValidationError

from database import SessionLocal
from schemas import TokenPayload, SystemAccount


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@lru_cache()
def get_settings():
  return utils.Settings()


reuseable_oauth = OAuth2PasswordBearer(
  tokenUrl="/login",
  scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth),db: Session = Depends(get_db),
                           settings: utils.Settings = Depends(get_settings)) -> SystemAccount:
  try:
    payload = jwt.decode(
      token, settings.jwt_secret_key, algorithms=[settings.algorithm]
    )
    token_data = TokenPayload(**payload)

    if datetime.fromtimestamp(token_data.exp) < datetime.now():
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
        headers={"WWW-Authenticate": "Bearer"},
      )
  except(jwt.JWTError, ValidationError):
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
    )
  username: str = token_data.sub
  # get user from database
  user = repository.get_account_by_username(db, username=username)
  # if user does not exist, raise an exception
  if not user:
    raise HTTPException(status_code=404, detail="user does not exists")
  # if user exist, return user Schema with password hashed
  return SystemAccount(**user)

"""

from fastapi.security import OAuth2PasswordBearer
from pydantic.tools import lru_cache

import utils


@lru_cache()
def get_settings():
    return utils.Settings()


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)
