from importlib.metadata import PackageNotFoundError, version

from fastapi import FastAPI

from src.routes.health import router as health_router
from src.routes.locations import router as location_router

try:
    app_version = version("weather-api")
except PackageNotFoundError:
    app_version = "0.0.0-dev"

app = FastAPI(title="Weather API", description="A simple weather API", version=app_version)
app.include_router(location_router)
app.include_router(health_router)
