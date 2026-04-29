from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from src.routes import upload, chat

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists(UPLOAD_DIR):
        os.mkdir(UPLOAD_DIR)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def fun():
    return "server is up and running"

app.include_router(router=upload.router)
app.include_router(router=chat.router)