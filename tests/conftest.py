import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src import Base
from src.config import settings
from src.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(
        app=app, base_url="http://test", follow_redirects=True
    ) as async_client:
        yield async_client


@pytest.fixture(scope="session")
def engine():
    db_url = (
        f"postgresql+asyncpg://"
        f"{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )
    engine = create_async_engine(db_url, future=True)
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture()
async def create_tables(engine):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def test_db(engine):
    async_session = AsyncSession(engine, expire_on_commit=False)
    yield async_session
    await async_session.close()
