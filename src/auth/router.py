from fastapi import APIRouter, Form, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

import user.models as user_models
import auth.service as auth_service
import database


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
    return {
        "username": user.username,
    }