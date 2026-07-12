# Weather API

A REST API for location-based weather monitoring, built as part of the Cloud Computing course at HAW Kiel.

## Purpose

The goal of this project is not just to build a working weather API, but to design, test, and deploy it the way a production service would be: with a clean application structure, automated tests, containerization, and a Kubernetes-based deployment.

The application lets users define locations (via latitude/longitude) and metrics to track, then ingests weather data for those locations from [Open-Meteo](https://open-meteo.com/)'s forecast endpoint. Measurements and forecasts are stored in a single unified table, distinguished by a `forecast_horizon` column (0 for the current hour, positive values for forecasts further ahead).

**Note on historical data:** Backfilled past data reflects today's forecast run applied retroactively, not the forecast that was actually issued at the time, or the actually observed value. Genuine forecast-horizon diversity for past timestamps only builds up over time, through the daily forecast CronJob repeatedly snapshotting the same future timestamps on different days. A helper script (see below) can simulate this for demo purposes.

## Features

- Locations, metrics, and measurements as a REST API (full CRUD for locations and metrics, filtered reads for measurements)
- User authentication (register/login/me) via JWT bearer tokens; write operations on locations and metrics require authentication
- Automatic 30-day historical backfill and forecast data when a location or metric is created
- Automated ongoing data ingestion via Kubernetes CronJobs: hourly (current measurements) and daily (forecast updates)
- Metric names are validated against Open-Meteo's supported variables (statically, and optionally live)
- Offline fallback: a pre-captured sample dataset is loaded automatically if `ONLINE=false`, so the API is usable without internet access

## Tech Stack

- **API**: FastAPI, Pydantic / pydantic-settings
- **Database**: PostgreSQL, SQLAlchemy 2.0 (ORM), Alembic migrations
- **Auth**: Argon2 password hashing, JWT bearer tokens
- **Data ingestion**: openmeteo-requests (official Open-Meteo client)
- **Testing**: pytest (unit tests for pure business logic, integration tests against a real Postgres instance)
- **Tooling**: uv, ruff, pre-commit
- **CI/CD**: GitHub Actions, release-please
- **Deployment**: Docker, Kubernetes (Kustomize, kind for local development)

## Project Status

The core API (locations, metrics, measurements, auth) is implemented and tested. Data ingestion (backfill, hourly/daily CronJobs, offline fallback) is implemented. 

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
6. The API is now reachable at `http://localhost:8000`

Database migrations run automatically on container startup (see `entrypoint.sh`), no manual `alembic upgrade head` needed.

On first startup, the app automatically seeds two metrics (`temperature_2m`, `rain`) and one location (CERN Geneva), backfilling 30 days of history plus forecast data, unless a location already exists (idempotent across restarts) or `ONLINE=false` (see below).

### Working with the API

Most read endpoints (`GET /locations`, `GET /metrics`, `GET /locations/{id}/measurements`, ...) require no authentication. Creating, updating, or deleting locations and metrics requires a registered user:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "supersecret123"}'

curl -X POST http://localhost:8000/auth/login \
  -d "username=you@example.com&password=supersecret123"
```

Use the returned `access_token` as a `Bearer` token on subsequent requests. Interactive docs are available at `http://localhost:8000/docs`.

### Offline mode

Set `ONLINE=false` in `secret/.env` before the first startup to skip live Open-Meteo calls entirely. In this mode, the app loads a static, pre-captured sample dataset (`db/sample_dump.sql`) instead of performing a live backfill, and metric name validation falls back to a static list instead of checking against the live API.

### Simulating forecast history (optional)

Because backfilled historical data has no real horizon diversity (see the note under Purpose), `scripts/simulate_forecast_history.py` can artificially populate several days of forecast snapshots for testing/demo purposes:

```bash
uv run python -m scripts.simulate_forecast_history --days-back 10
```

This is a demo/testing aid only; the values it produces reflect today's forecast, backdated, not historically accurate forecasts.

## Author

Yannik Krantz