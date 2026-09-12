from datetime import datetime
from datetime import timedelta

from jose import jwt
from pwdlib import PasswordHash

SECRET_KEY = "CHANGE_THIS_TO_A_64_CHARACTER_SECRET"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(password, hashed):
    return password_hash.verify(password, hashed)


def create_access_token(user_id):

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": expire,
            "type": "access",
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def create_refresh_token(user_id):

    expire = datetime.utcnow() + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": expire,
            "type": "refresh",
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )