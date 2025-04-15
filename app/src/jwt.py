import os
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi import HTTPException

SECRET = str(os.getenv("JWT_SECRET"))
ALGORITHM = "HS256"

def create_jwt(data: dict) -> str:
    return jwt.encode(data, SECRET, algorithm=ALGORITHM)

def decode_jwt(token: str) -> dict | bool:
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except InvalidTokenError or ExpiredSignatureError:
        raise HTTPException(401, detail="Unathorizated")