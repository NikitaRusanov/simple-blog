import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src import User

import src.auth.utils as auth_utils


@pytest.fixture()
async def user_test_samples(test_db: AsyncSession, create_tables):
    samples = [
        User(
            email=f"test_email_{num}@mail.com",
            username=f"test_user_{num}",
            password=f"test_password_{num}",
        )
        for num in range(1, 4)
    ]

    test_db.add_all(samples)
    await test_db.commit()
    yield samples


@pytest.fixture()
async def get_user(test_db: AsyncSession, create_tables):
    async def _get_user(id: int):
        test_db.expire_all()
        user = await test_db.get(User, id)
        return user

    yield _get_user
    await test_db.close()


@pytest.fixture()
async def test_auth_headers(test_db: AsyncSession, create_tables):
    test_user = User(
        email="token_test_user@mail.com",
        username="token_test_user",
        password="test_password",
    )
    test_db.add(test_user)
    await test_db.commit()

    test_token = auth_utils.encode_token(
        payload={
            "sub": test_user.id,
            "username": test_user.username,
            "email": test_user.email,
        }
    )

    headers = {"Authorization": f"Bearer {test_token}"}
    yield headers
