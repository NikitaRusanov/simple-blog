from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import user.models as user_models


async def get_user_by_name(
    username: str, session: AsyncSession
) -> user_models.User | None:

    user = await session.scalars(
        select(user_models.User).where(user_models.User.username == username)
    )
    return user.one_or_none()


async def validate_user(
    username: str,
    password: str,
    session: AsyncSession
) -> user_models.User | None:
    
    user = await get_user_by_name(username, session)
    if not user or user.password != password:
        return
    return user
