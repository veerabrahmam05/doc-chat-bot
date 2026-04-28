from fastapi import FastAPI

from src.routes import upload, chat

app = FastAPI()

@app.get("/")
def fun():
    return "server is up and running"

app.include_router(router=upload.router)
app.include_router(router=chat.router)