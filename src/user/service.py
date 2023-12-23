from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import User
from .schemas import UserIn


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).order_by(User.id))
    result = list(result.scalars().all())
    await session.close()
    return result


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    user = await session.get(User, user_id)
    await session.close()
    return user


async def create_user(session: AsyncSession, user_in: UserIn) -> User:
    user = User(**(user_in.model_dump()))
    session.add(user)
    await session.commit()
    
    return user