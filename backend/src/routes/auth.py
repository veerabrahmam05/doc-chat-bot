from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from src.config.env import settings
from src.models.schemas import User as UserDoc
from src.models.models import Token, UserInDB as UserModel, User as UserResponse
from src.services.auth_service import authenticate_user, create_access_token, hash_password

DATABASE_URL = settings.database_url
JWT_SECRET = settings.jwt_secret
JWT_ALGORITHM = settings.jwt_algorithm
TOKEN_EXPIRES_IN = settings.token_expires_in

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=Token)
async def login(formdata: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(formdata.username, formdata.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalide username or password",
            headers={ "WWW-Authenticate": "Bearer" }
        )
    
    token_expires_in = timedelta(minutes=TOKEN_EXPIRES_IN)
    access_token = create_access_token({ "sub": user.username }, token_expires_in)

    return Token(
        access_token=access_token,
        token_type="Bearer"
    )

@router.post("/signup", response_model=UserResponse)
async def create_new_user(user_data: UserModel):
    hashed_password = hash_password(user_data.password)
    user_doc = UserDoc(username=user_data.username, email=user_data.email, password=hashed_password)
    await user_doc.insert()
    # Return a UserResponse (Pydantic) without password
    return UserResponse(username=user_doc.username, email=user_doc.email)