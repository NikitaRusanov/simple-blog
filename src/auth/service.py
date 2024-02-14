from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import Depends, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from jwt.exceptions import InvalidTokenError

import user.models as user_models
import auth.utils as auth_utils
import user.service as user_service
from database import database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def get_user_by_name(
    username: str, session: AsyncSession
) -> user_models.User | None:

    user = await session.scalars(
        select(user_models.User).where(user_models.User.username == username)
    )
    return user.one_or_none()


async def validate_user(
    username: str, password: str, session: AsyncSession
) -> user_models.User | None:

    user = await get_user_by_name(username, session)
    if not user or user.password != password:
        return
    return user


async def get_user_from_token(
    session: AsyncSession = Depends(database.scoped_session_dependency),
    token: str = Depends(oauth2_scheme),
) -> user_models.User | None:

    auth_err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    )
    try:
        payload = auth_utils.decode_token(token)
    except InvalidTokenError as e:
        raise auth_err

    user_id = int(payload.get("sub"))  # type: ignore
    if not (user := await user_service.get_user(session, user_id)):
        raise auth_err
    return user
