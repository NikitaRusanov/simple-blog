import pytest

from src.database import database
from src import Base


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    async with database.engine.begin() as conenction:
        await conenction.run_sync(Base.metadata.create_all)