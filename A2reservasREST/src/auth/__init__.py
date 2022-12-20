from typing import Any, List
from fastapi import Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from jose.jwt import decode

from ..settings import Settings
from ..beans import get_settings, get_public_key

class AuthenticationError(Exception):
    pass


class Claims(BaseModel):
    sub: str
    exp: int
    iat: int
    iss: str

scheme = HTTPBearer()


def Authentication(
    credentials: HTTPBearer = Depends(scheme),
    keys: List[Any] = Depends(get_public_key),
    settings: Settings = Depends(get_settings)
) -> Claims:
    token: str = credentials.credentials

    try:
        payload = decode(
            token, 
            key=keys,
            audience=settings.auth.audience
        )
        return Claims(**payload)
    except Exception as e:
        print(e)
        raise AuthenticationError(e)