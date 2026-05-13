from pymongo import AsyncMongoClient
from beanie import init_beanie
from src.models.schemas import User, Conversation
from src.config.env import settings

async def init_db():
    client = AsyncMongoClient(settings.database_url)
    # Use the database specified in the connection string (MongoDB driver picks the default DB)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[User, Conversation])
