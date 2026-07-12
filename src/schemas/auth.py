from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Payload for registering a new user.

    Attributes:
        email: The user's email address, used as their unique identifier.
        password: The user's plaintext password, hashed before storage.
    """

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserPublic(BaseModel):
    """Public representation of a user, never includes the password hash.

    Attributes:
        id: Unique identifier assigned by the database.
        email: The user's email address.
    """

    id: int
    email: EmailStr


class Token(BaseModel):
    """Bearer token returned after a successful login.

    Attributes:
        access_token: The signed JWT.
        token_type: The token type, always "bearer".
    """

    access_token: str
    token_type: str = "bearer"
