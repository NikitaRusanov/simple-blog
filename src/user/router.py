from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import user.service as service
import user.schemas as schemas
from database import database
from user import dependencies
from user import models
import auth.service as auth_service

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[schemas.UserOut])
async def get_users(
    session: AsyncSession = Depends(database.scoped_session_dependency),
    current_user=Depends(auth_service.get_user_from_token),
):
    return await service.get_users(session=session)


@router.post("/", response_model=schemas.UserOut, status_code=201)
async def create_user(
    user_in: schemas.UserIn,
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    new_user = await service.create_user(session=session, user_in=user_in)
    return new_user


@router.get("/me", response_model=schemas.UserOut)
async def get_current_user(
    user: models.User = Depends(auth_service.get_user_from_token),
):
    return user


@router.get("/{user_id}", response_model=schemas.UserOut)
async def get_user(
    current_user=Depends(auth_service.get_user_from_token),
    user: schemas.UserOut = Depends(dependencies.get_user_by_id),
):
    return user


@router.patch("/{user_id}", response_model=schemas.UserOut)
async def update_user(
    user_update: schemas.UserUpdate,
    session: AsyncSession = Depends(database.scoped_session_dependency),
    current_user=Depends(auth_service.get_user_from_token),
    user: models.User = Depends(dependencies.get_user_by_id),
):
    return await service.update_user(
        session=session, user=user, user_update=user_update
    )


@router.delete("/{user_id}")
async def delete_user(
    session: AsyncSession = Depends(database.scoped_session_dependency),
    current_user=Depends(auth_service.get_user_from_token),
    user: models.User = Depends(dependencies.get_user_by_id),
):
    await service.delete_user(session, user)
    return JSONResponse(content={"detail": "OK"}, status_code=status.HTTP_200_OK)
