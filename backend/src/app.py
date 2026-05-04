from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from src.routes import upload, chat
from src.config.env import settings

UPLOAD_DIR = settings.upload_dir

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists(UPLOAD_DIR):
        os.mkdir(UPLOAD_DIR)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def fun():
    return "server is up and running"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(router=upload.router)
app.include_router(router=chat.router)