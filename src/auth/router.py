from fastapi import APIRouter, Form, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from jwt.exceptions import InvalidTokenError

import user.models as user_models
import auth.service as auth_service
import database
import auth.utils as auth_utils
import user.service as user_servie


router = APIRouter(tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def validate_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(database.database.scoped_session_dependency),
) -> user_models.User:

    if user := await auth_service.validate_user(username, password, session):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong username or password"
    )


@router.post("/login/")
async def login(user: user_models.User = Depends(validate_user)):
    token_payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_token(token_payload)
    return {"access_token": token, "token_type": "Bearer"}


async def get_user_from_token(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(database.database.scoped_session_dependency),
) -> user_models.User | None:

    auth_err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    )
    try:
        payload = auth_utils.decode_token(token)
    except InvalidTokenError as e:
        raise auth_err

    user_id = int(payload.get("sub"))  # type: ignore
    if not (user := await user_servie.get_user(session, user_id)):
        raise auth_err
    return user
