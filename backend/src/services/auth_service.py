import jwt
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, password: str):
    return password_hash.verify(plain_password, password)

def hash_password(plain_password: str):
    return password_hash.hash(plain_password)

