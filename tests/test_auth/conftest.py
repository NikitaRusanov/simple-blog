from typing import Generator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src import User
import src.auth.utils as auth_utils

USER_DATA = {
    "username": "test_user",
    "password": "test_pass",
    "email": "test@mail.com"
}


@pytest.fixture
async def create_user(test_db: AsyncSession, create_tables):
    test_user = User(username=USER_DATA["username"], email=USER_DATA["email"],
                     password=auth_utils.hash_password(USER_DATA["password"]))
    test_db.add(test_user)
    await test_db.commit()
    yield test_user
