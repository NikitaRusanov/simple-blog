from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings


class Database:
    
    def __init__(self, url: str, echo: bool) -> None:
        self.engine = create_async_engine(
            url,
            echo=echo
        )
        self.get_session = async_sessionmaker(
            bind=self.engine,
            autoflush=False, 
            autocommit=False,
            expire_on_commit=False,
        )


url = f'postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
database = Database(url, settings.debug)
