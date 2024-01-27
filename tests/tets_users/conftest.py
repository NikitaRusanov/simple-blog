import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src import User


@pytest.fixture()
async def user_test_samples(test_db: AsyncSession, create_tables):
    samples = [
        User(
            email=f'test_email_{num}@mail.com',
            username=f'test_user_{num}',
            password=f'test_password_{num}'
        )
        for num in range(1, 4)
    ]

    test_db.add_all(samples)
    await test_db.commit()
    yield samples


@pytest.fixture()
async def get_user(test_db: AsyncSession, create_tables):
    async def _get_user(id: int):
        user = await test_db.get(User, id)
        await test_db.refresh(user)
        return user
    yield _get_user
    await test_db.close()
        

