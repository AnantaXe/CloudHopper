from datetime import datetime
from datetime import timedelta

from fastapi import APIRouter, FastAPI
from fastapi import Depends
from fastapi import HTTPException

# from rich.align import console
from rich import _console
from sqlalchemy.orm import Session
from typer.cli import app

from database.database import SessionLocal
from shared.models.authorization.models import User

from security.security import hash_password
from security.security import verify_password
from security.security import create_access_token
from security.security import create_refresh_token
from shared.models.api_req_schemas import LoginRequest, RegisterRequest
from security.session_manager import SessionManager
from opentelemetry import trace

router = APIRouter()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def check_if_user_already_exists(db: Session, username: str, email: str):
    user = (
        db.query(User)
        .filter((User.username == username) | (User.email == email))
        .first()
    )

    if user:
        raise HTTPException(
            400,
            "User with this username or email already exists",
        )


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

    check_if_user_already_exists(db, request.username, request.email)

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

    SessionManager.set_session_data({
        "user_id": user.id,
        "access_token": access,
        "refresh_token": refresh,
    })
    
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer",
    }