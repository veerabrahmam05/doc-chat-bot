import jwt
from pwdlib import PasswordHash
from datetime import timedelta, timezone, datetime

from src.models.schemas import User
from src.config.env import settings

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