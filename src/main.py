import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import database
import models
from user.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    yield

app = FastAPI(title='Simple Blog', lifespan=lifespan)

app.include_router(user_router, prefix='/user')


if __name__ == '__main__':
    uvicorn.run('main:app')

         


