from sqlalchemy.orm import Session

from src.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError
from src.models import User
from src.repositories import user_repository
from src.security import create_access_token, hash_password, verify_password


def register_user(db: Session, email: str, password: str) -> User:
    """Register a new user.

    Args:
        db: Database session.
        email: The email address to register.
        password: The plaintext password to hash and store.

    Returns:
        The newly created user.

    Raises:
        EmailAlreadyRegisteredError: If the email is already registered.
    """
    if user_repository.get_by_email(db, email) is not None:
        raise EmailAlreadyRegisteredError(email)

    return user_repository.create(db, email, hash_password(password))


def authenticate_user(db: Session, email: str, password: str) -> str:
    """Authenticate a user and issue an access token.

    Args:
        db: Database session.
        email: The email address to authenticate.
        password: The plaintext password to verify.

    Returns:
        A signed JWT access token.

    Raises:
        InvalidCredentialsError: If the email or password is incorrect.
    """
    user = user_repository.get_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError()

    return create_access_token(subject=user.email)
