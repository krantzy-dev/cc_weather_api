from datetime import UTC, datetime, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.config import settings

_hasher = PasswordHasher()


def hash_password(plain: str) -> str:
    """Hash a plaintext password with Argon2, applying the app-wide pepper."""
    material = f"{plain}{settings.auth_pepper}"
    return _hasher.hash(material)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against a stored Argon2 hash."""
    material = f"{plain}{settings.auth_pepper}"
    try:
        _hasher.verify(hashed, material)
        return True
    except VerifyMismatchError:
        return False


def create_access_token(subject: str) -> str:
    """Create a signed JWT access token for the given subject (typically an email)."""
    expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> str | None:
    """Decode a JWT access token and return its subject, or None if invalid."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError:
        return None
    subject = payload.get("sub")
    return subject if isinstance(subject, str) else None
