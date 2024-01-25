import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src import Base
from src.main import app
from src.config import settings


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client


db_url = (f'postgresql+asyncpg://'
          f'{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}')
engine = create_async_engine(db_url)


@pytest.fixture(scope='session', autouse=True)
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        yield
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def test_db():
    async_session = AsyncSession(engine)
    yield async_session
    await async_session.close()