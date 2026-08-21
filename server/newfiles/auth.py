from datetime import datetime
from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import SessionLocal
from models import User

from security import hash_password
from security import verify_password
from security import create_access_token
from security import create_refresh_token
from schemas import LoginRequest, RegisterRequest

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

    user = User(
        username=request.username,
        email=request.email,
        password_hash=hash_password(request.password),
    )

    db.add(user)

    db.commit()

    return {"message": "User created"}


@router.post("/login")
def login(
    request: LoginRequest   ,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(User.username == request.username)
        .first()
    )

    if not user:

        raise HTTPException(401, "Invalid credentials")

    if user.account_locked_until:

        if user.account_locked_until > datetime.utcnow():

            raise HTTPException(
                403,
                "Account temporarily locked",
            )

    if not verify_password(
        request.password,
        user.password_hash,
    ):

        user.failed_login_attempts += 1

        if user.failed_login_attempts >= 5:

            user.account_locked_until = (
                datetime.utcnow()
                + timedelta(minutes=15)
            )

        db.commit()

        raise HTTPException(
            401,
            "Invalid credentials",
        )

    user.failed_login_attempts = 0

    db.commit()

    access = create_access_token(user.id)

    refresh = create_refresh_token(user.id)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer",
    }