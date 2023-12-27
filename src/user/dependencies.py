from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    Depends,
    Path,
    HTTPException,
    status
    )

from database import database
from user.models import User
from user import service


async def get_user_by_id(
        user_id: Annotated[int, Path],
        session: AsyncSession = Depends(database.scoped_session_dependency)) -> User:
    
    if user := await service.get_user(session=session, user_id=user_id):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {user_id} not found'
        )
    