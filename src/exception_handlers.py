from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    InvalidTokenError,
    LocationTooCloseError,
    MetricAlreadyExistsError,
    UnsupportedMetricError,
)


async def location_too_close_handler(request: Request, exc: LocationTooCloseError) -> JSONResponse:
    """Translate a LocationTooCloseError into a 409 Conflict response."""
    return JSONResponse(status_code=409, content={"detail": str(exc)})


async def email_already_registered_handler(
    request: Request, exc: EmailAlreadyRegisteredError
) -> JSONResponse:
    """Translate an EmailAlreadyRegisteredError into a 409 Conflict response."""
    return JSONResponse(status_code=409, content={"detail": str(exc)})


async def invalid_credentials_handler(
    request: Request, exc: InvalidCredentialsError
) -> JSONResponse:
    """Translate an InvalidCredentialsError into a 401 Unauthorized response."""
    return JSONResponse(
        status_code=401,
        content={"detail": "incorrect email or password"},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def invalid_token_handler(request: Request, exc: InvalidTokenError) -> JSONResponse:
    """Translate an InvalidTokenError into a 401 Unauthorized response."""
    return JSONResponse(
        status_code=401,
        content={"detail": "invalid or expired token"},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def metric_already_exists_handler(
    request: Request, exc: MetricAlreadyExistsError
) -> JSONResponse:
    """Translate a MetricAlreadyExistsError into a 409 Conflict response."""
    return JSONResponse(status_code=409, content={"detail": str(exc)})


async def unsupported_metric_handler(request: Request, exc: UnsupportedMetricError) -> JSONResponse:
    """Translate an UnsupportedMetricError into a 422 Unprocessable Entity response."""
    return JSONResponse(status_code=422, content={"detail": str(exc)})


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom domain exception handlers on the given app.

    Args:
        app: The FastAPI application instance to register handlers on.
    """
    app.add_exception_handler(LocationTooCloseError, location_too_close_handler)
    app.add_exception_handler(EmailAlreadyRegisteredError, email_already_registered_handler)
    app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
    app.add_exception_handler(InvalidTokenError, invalid_token_handler)
    app.add_exception_handler(MetricAlreadyExistsError, unsupported_metric_handler)
    app.add_exception_handler(UnsupportedMetricError, unsupported_metric_handler)
