from beanie import Document, Indexed
from pydantic import EmailStr

class User(Document):
    username: str
    email: EmailStr
    password: str

    class Settings:
        name = "users"
        # Collection name in MongoDB
