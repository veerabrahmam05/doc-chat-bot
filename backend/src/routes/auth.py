from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from src.config.env import settings
from src.config.db import get_db
from src.services.auth_service import authenticate_user, create_access_token, hash_password
from src.models.models import Token, UserInDB as UserModel, User as UserResponse
from src.models.schemas import User as UserSchema

DATABASE_URL = settings.database_url
JWT_SECRET = settings.jwt_secret
JWT_ALGORITHM = settings.jwt_algorithm
TOKEN_EXPIRES_IN = settings.token_expires_in

router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token", response_model=Token)
def login(formdata: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_db)):
    user = authenticate_user(session, formdata.username, formdata.password)

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
def create_new_user(user_data: UserModel, session: Session = Depends(get_db)):
    hashed_password = hash_password(user_data.password)
    user = UserSchema(username=user_data.username, email=user_data.email, password=hashed_password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user