from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions import LocationTooCloseError


async def location_too_close_handler(request: Request, exc: LocationTooCloseError) -> JSONResponse:
    """Translate a LocationTooCloseError into a 409 Conflict response."""
    return JSONResponse(status_code=409, content={"detail": str(exc)})


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom domain exception handlers on the given app.

    Args:
        app: The FastAPI application instance to register handlers on.
    """
    app.add_exception_handler(LocationTooCloseError, location_too_close_handler)
