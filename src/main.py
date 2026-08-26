from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api import main_router
from src.database import migrate


@asynccontextmanager
async def lifespan(app: FastAPI):
    await migrate()
    yield


app = FastAPI(lifespan=lifespan)

# Фронтенд может быть на другом origin/порту — разрешаем кросс-доменные
# запросы к API (иконки в <img> не требуют CORS, только fetch /keys).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
app.mount("/icons", StaticFiles(directory="icons"), name="icons")
