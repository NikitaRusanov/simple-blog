import asyncio

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.config import settings
from src import Base


url = f'postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}'

@pytest.fixture(scope='session')
def event_lopp():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def engine():
    engine = create_async_engine(url)
    print(url)
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture
async def async_session(engine):
    async with AsyncSession(engine) as session:
        yield session


@pytest.fixture(scope='function', autouse=True)
async def setup_db(engine):
    async with engine.begin() as conenction:
        await conenction.run_sync(Base.metadata.drop_all)
    yield
    async with engine.begin() as conenction:
        await conenction.run_sync(Base.metadata.create_all)