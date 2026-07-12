from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import User


def get_by_email(db: Session, email: str) -> User | None:
    """Retrieve a user by email, case-insensitively.

    Args:
        db: Database session.
        email: The email address to look up.

    Returns:
        The matching user, or None if no such user exists.
    """
    return db.execute(select(User).where(User.email == email.lower())).scalar_one_or_none()


def create(db: Session, email: str, password_hash: str) -> User:
    """Insert a new user.

    Args:
        db: Database session.
        email: The user's email address, stored lowercased.
        password_hash: The already-hashed password.

    Returns:
        The newly created, persisted user.
    """
    user = User(email=email.lower(), password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
