import jwt
from pwdlib import PasswordHash
from datetime import timedelta, timezone, datetime
from fastapi import status, HTTPException, Depends

from src.models.schemas import User
from src.models.models import TokenData
from src.config.env import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm

password_hash = PasswordHash.recommended()

dummy_password = password_hash.hash("dummy_password")

def verify_password(plain_password: str, password: str):
    return password_hash.verify(plain_password, password)

def hash_password(plain_password: str):
    return password_hash.hash(plain_password)

async def get_user(username: str):
    return await User.find_one(User.username == username)

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        # Mitigate timing attacks by performing fake verification
        verify_password(password, dummy_password)
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expires_in = datetime.now(timezone.utc) + expires_delta
    to_encode.update({ "exp": expires_in })
    
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_errors = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid user credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise credential_errors
        token_data = TokenData(username=username)
    except Exception:
        raise credential_errors

    user = await User.find_one(User.username == token_data.username)

    if user is None:
        raise credential_errors

    return user