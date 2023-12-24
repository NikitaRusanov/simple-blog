from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,

    )
from asyncio import current_task


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

    def get_scoped_session(self):
            session = async_scoped_session(
                session_factory=self.get_session,
                scopefunc=current_task
            )
            return session
        
    async def session_dependency(self) -> AsyncSession: # type: ignore
        async with self.get_session() as session: 
            yield session  # type: ignore
            await session.close()


url = f'postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
database = Database(url, settings.debug)
