import tomllib
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from src.database import SessionLocal
from src.exception_handlers import register_exception_handlers
from src.load_data.initial_load import run_initial_load
from src.routes.auth import router as auth_router
from src.routes.health import router as health_router
from src.routes.locations import router as location_router
from src.routes.measurements import router as measurement_router
from src.routes.metrics import router as metric_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run one-time startup tasks, then hand control back to the app."""
    db = SessionLocal()
    try:
        run_initial_load(db)
    finally:
        db.close()
    yield


def get_app_version() -> str:
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    try:
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]
    except (FileNotFoundError, KeyError):
        return "0.0.0-dev"


app_version = get_app_version()

app = FastAPI(
    title="Weather API", description="A simple weather API", version=app_version, lifespan=lifespan
)
app.include_router(location_router)
app.include_router(metric_router)
app.include_router(measurement_router)
app.include_router(auth_router)
app.include_router(health_router)

register_exception_handlers(app)
