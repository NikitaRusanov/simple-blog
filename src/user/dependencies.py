from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import database
from user import service
from user.models import User


async def get_user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(database.scoped_session_dependency),
) -> User:
    if user := await service.get_user(session=session, user_id=user_id):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
