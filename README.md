# Weather API

A REST API for location-based weather monitoring, built as part of the Cloud Computing course at HAW Kiel.

## Purpose

The goal of this project is not just to build a working weather API, but to design, test, and deploy it the way a production service would be: with a clean application structure, automated tests, containerization, and a Kubernetes-based deployment.

The application lets users define locations (via latitude/longitude) and metrics to track, then ingests both historical measurements and forecasts for those locations from [Open-Meteo](https://open-meteo.com/) (forecast and archive endpoints, no API key required). Measurements and forecasts are stored in a single unified table, distinguished by a `forecast_horizon` column, so historical forecast accuracy can be analyzed later.

## Planned Features

- Define and manage locations and metrics
- Automated data ingestion (hourly current measurements, daily forecast backfills) via Kubernetes CronJobs
- Query measurements with filters (time range, metric, forecast horizon)
- User authentication for managing locations and metrics
- Seed dataset for demo purposes if live data ingestion is unavailable

## Tech Stack (planned)

- **API**: FastAPI, Pydantic / pydantic-settings
- **Database**: PostgreSQL, SQLAlchemy ORM, Alembic migrations
- **Testing**: pytest
- **Tooling**: uv, ruff, pre-commit
- **CI/CD**: GitHub Actions, release-please
- **Deployment**: Docker, Kubernetes (kind for local development)

## Project Status

This project is under active development. The application structure (configuration, logging, tooling) is currently being set up before the database layer and API routes are implemented. A detailed "Getting Started" section will be added here once the initial setup is stable enough for others to run the project locally.

## Getting Started

### Requires
- uv (>=0.9.8)
- Docker
- kind
- kubectl

### Run
1. Run `uv sync` in the project root
2. Run `uv run pre-commit install` and `uv run pre-commit run --all-files` once
3. Copy `secret/.env.example` to `secret/.env` and set the desired values. These are used by both the Python project (locally) and by Kustomize's `secretGenerator` when deploying to `dev`
4. Run `kind create cluster --config kind-config.yaml`
5. Run `kubectl apply -k k8s/overlays/dev`
6. Run `uv run alembic upgrade head` to apply database migrations
7. The API is now reachable at `http://localhost:8000`
8. In case dummy data is needed for functionality of certain routes run `uv run python -m scripts.simulate_forecast_history --days-back 10`

## Author

Yannik Krantz