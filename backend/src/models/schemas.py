from beanie import Document
from pydantic import EmailStr
from typing import Optional, List
from bson import ObjectId
from datetime import datetime
from pydantic import Field


from pydantic import ConfigDict

class User(Document):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    username: str
    email: EmailStr
    password: str

    class Settings:
        name = "users"
        # Collection name in MongoDB


class Conversation(Document):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    user_id: Optional[ObjectId] = None  # reference to User, optional for unauthenticated
    doc_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List[dict] = Field(default_factory=list)

    class Settings:
        name = "conversations"
        # Collection name in MongoDB

