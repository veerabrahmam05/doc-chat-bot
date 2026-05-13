from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class User(BaseModel):
    username: str
    email: str

class UserInDB(User):
    password: str

    model_config = { 'from_attributes': True}

class ChatRequest(BaseModel):
    doc_id: str
    question: str
    conversation_id: Optional[str] = None  # UUID of conversation, optional
