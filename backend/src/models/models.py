from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str

class UserInDB(User):
    password: str

    model_config = { 'from_attributes': True}

class ChatRequest(BaseModel):
    doc_id: str
    question: str