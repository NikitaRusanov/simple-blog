from datetime import datetime, timedelta, UTC

import jwt

import bcrypt

from config import settings


def encode_token(
    payload: dict,
    private_key: str = settings.private_key_path.read_text(),
    algorithm: str = settings.algorithm,
    expire_time: int = settings.token_expire_minutes,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    to_encode.update(exp=now + timedelta(minutes=expire_time), iat=now)

    token = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return token


def decode_token(
    token: str,
    public_key: str = settings.public_key_path.read_text(),
    algorithm: str = settings.algorithm,
) -> dict:
    data = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    return data


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    pwd_hashed = bcrypt.hashpw(password.encode(), salt)
    return pwd_hashed.decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
