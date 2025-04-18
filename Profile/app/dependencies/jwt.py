from dataclasses import dataclass

from fastapi import HTTPException, Request
import jwt

from app.config import config


@dataclass
class JWTPayload:
    sub: str
    role: str
    jti: str
    exp: int


async def get_uuid_from_token(request: Request) -> JWTPayload:
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Invalid authorization scheme")

    token = auth_header.split("Bearer ")[1]

    SECRET_KEY = config.jwt_key

    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={
        "verify_exp": False, "verify_aud": False})

    return JWTPayload(sub=decoded_payload["sub"], role=decoded_payload["role"], jti=decoded_payload["jti"], exp=decoded_payload["exp"])
