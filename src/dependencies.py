from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.database import get_db
from src.exceptions import InvalidTokenError
from src.models import User
from src.repositories import user_repository
from src.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Resolve the currently authenticated user from a bearer token.

    Args:
        token: The bearer token, extracted automatically from the request.
        db: Database session.

    Returns:
        The authenticated user.

    Raises:
        InvalidTokenError: If the token is invalid, expired, or no longer
            matches an existing user.
    """
    email = decode_access_token(token)
    if email is None:
        raise InvalidTokenError()

    user = user_repository.get_by_email(db, email)
    if user is None:
        raise InvalidTokenError()

    return user
