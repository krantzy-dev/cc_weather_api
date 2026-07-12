from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.dependencies import get_current_user
from src.models import User
from src.schemas.auth import Token, UserCreate, UserPublic
from src.services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=201,
    responses={409: {"description": "Email already registered"}},
)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    """Register a new user account."""
    return register_user(db, payload.email, payload.password)


@router.post(
    "/login",
    response_model=Token,
    responses={401: {"description": "Incorrect email or password"}},
)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    """Log in and receive a bearer access token.

    Uses the OAuth2 password flow: send `username` (the email) and
    `password` as form fields.
    """
    token = authenticate_user(db, form.username, form.password)
    return Token(access_token=token)


@router.get("/me", response_model=UserPublic)
def read_me(current_user: User = Depends(get_current_user)) -> User:
    """Return the currently authenticated user's public profile."""
    return current_user
