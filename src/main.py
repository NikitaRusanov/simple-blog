from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

import models
from auth.router import router as auth_router
from database import database
from user.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(title="Simple Blog", lifespan=lifespan)


@app.get("/")
def index():
    return {"msg": "API works properly"}


app.include_router(user_router, prefix="/user")
app.include_router(auth_router, prefix="/auth")


if __name__ == "__main__":
    fake = ""
    uvicorn.run("main:app")
