from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

