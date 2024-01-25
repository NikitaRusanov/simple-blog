from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from user.models import User
from user.schemas import UserIn, UserUpdate


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


async def update_user(session: AsyncSession, user: User, user_update: UserUpdate) -> User:
    result = await session.execute(
        update(User)
        .where(User.id == user.id)
        .values(user_update.model_dump(exclude_unset=True))
        .returning(User)
        )
    user = result.scalar_one()
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()