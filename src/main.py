import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api import main_router


app = FastAPI()
app.include_router(main_router)
app.mount("/icons", StaticFiles(directory="icons"), name="icons")