from importlib.metadata import PackageNotFoundError, version

from fastapi import FastAPI

try:
    app_version = version("weather-api")
except PackageNotFoundError:
    app_version = "0.0.0-dev"

app = FastAPI(title="Weather API", description="A simple weather API", version=app_version)
