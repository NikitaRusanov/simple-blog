from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
    )
from sqlalchemy.ext.asyncio import AsyncSession

import user.service as service
import user.schemas as schemas
from database import database


router = APIRouter(tags=['Users'])


@router.get('/', response_model=list[schemas.UserOut])
async def get_users(session: AsyncSession = Depends(database.session_dependency)):
    return await service.get_users(session=session)


@router.post('/', response_model=schemas.UserOut)
async def create_user(user_in: schemas.UserIn, session: AsyncSession = Depends(database.session_dependency)):
    new_user = await service.create_user(session=session, user_in=user_in)
    return new_user


@router.get('/{user_id}', response_model=schemas.UserOut)
async def get_user(user_id: int, session: AsyncSession = Depends(database.session_dependency)):
    if user := await service.get_user(session=session, user_id=user_id):
        print(user)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {user_id} not found'
        )
    

