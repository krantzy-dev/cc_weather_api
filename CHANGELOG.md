# Changelog

## [0.3.0](https://github.com/krantzy-dev/cc_weather_api/compare/v0.2.2...v0.3.0) (2026-07-11)


### Features

* **DB:** add SQLAlchemy models and initial Alembic migration ([6255677](https://github.com/krantzy-dev/cc_weather_api/commit/6255677f3dc936ef6699e824cbb9c8cd5c2196ed))
* **health:** add health check endpoints for liveness and readiness ([a579d06](https://github.com/krantzy-dev/cc_weather_api/commit/a579d066484449f04fe593060122055edadf7c7a))
* **test:** add pytest with initial fixtures for db sessions ([01e9ac4](https://github.com/krantzy-dev/cc_weather_api/commit/01e9ac443606bbfbd9bb52de6201862fbbbc0b19))

## [0.2.2](https://github.com/krantzy-dev/cc_weather_api/compare/v0.2.1...v0.2.2) (2026-07-10)


### Bug Fixes

* **infra:** add sync-uv-lock workflow for automatic uv.lock synchronization ([8ee4845](https://github.com/krantzy-dev/cc_weather_api/commit/8ee4845d0f0fd4e37ac49932f628faf47164b8b6))

## [0.2.1](https://github.com/krantzy-dev/cc_weather_api/compare/v0.2.0...v0.2.1) (2026-07-10)


### Bug Fixes

* **ci:** correct release-please job outputs ([f9b55ed](https://github.com/krantzy-dev/cc_weather_api/commit/f9b55ed0e991cf6b28d0b5780fc81c6aa2e92861))

## [0.2.0](https://github.com/krantzy-dev/cc_weather_api/compare/v0.1.0...v0.2.0) (2026-07-10)


### Features

* **ci:** add build-and-push job to release-please workflow for Docker image automation ([4cbea33](https://github.com/krantzy-dev/cc_weather_api/commit/4cbea336ddf4925a74d58f3aec0a18c2c3148f42))
* **ci:** add release-please configuration files for automated releases ([ea9f221](https://github.com/krantzy-dev/cc_weather_api/commit/ea9f221e21afd7f1040b5e16ef54c81d0fd71b60))
* **config:** added config for python logger ([60fd820](https://github.com/krantzy-dev/cc_weather_api/commit/60fd8200108a59e0b597018ade4bc6a2ae40c8db))
* **config:** added log_level variable to config.py ([5f5b806](https://github.com/krantzy-dev/cc_weather_api/commit/5f5b806fd0faa4e2f9229da41abde41a931d53ad))
* **config:** Changed LogLevel to Literal and added support for RELOAD variable ([cfb66f9](https://github.com/krantzy-dev/cc_weather_api/commit/cfb66f9f02603cc6f2cbf454a0367a43b0e110e4))
* **dependencies:** add fastapi and update uvicorn dependencies in pyproject.toml and uv.lock ([ba15182](https://github.com/krantzy-dev/cc_weather_api/commit/ba151826884c6fe6c5705ff1a7beb183bd819979))
* **docker:** add Dockerfile for multi-stage build and runtime setup ([a1f2ab7](https://github.com/krantzy-dev/cc_weather_api/commit/a1f2ab7be0b4161b86532224bb8d03797fee83d2))
* **infra:** added .env and config.py to make environment variables or .env variables usable ([5c6d59c](https://github.com/krantzy-dev/cc_weather_api/commit/5c6d59ca8a2140640972dccab5745deeb9fc2532))
* **infra:** added pydantic and pydantic-settings ([6413a39](https://github.com/krantzy-dev/cc_weather_api/commit/6413a3954f376b0f712a0ddd765982b1d2c32e10))
* **infra:** initial commit ([10ea41a](https://github.com/krantzy-dev/cc_weather_api/commit/10ea41a2ffe48170856b3b89adb63fddb07735fe))
* **main:** implement uvicorn server setup and update dependencies ([be50c60](https://github.com/krantzy-dev/cc_weather_api/commit/be50c6091f321385ee63416334c6cc2a451d39f4))
* **pre-commit:** add ruff pre-commit configuration for linting and formatting ([35fdd59](https://github.com/krantzy-dev/cc_weather_api/commit/35fdd59a8554d9a7c9392b0ac09706431691fd40))
* **style:** added ruff and config for linting and ran ruff check with fix parameter for the first time ([591ecea](https://github.com/krantzy-dev/cc_weather_api/commit/591ecea07322fdc369db02da000224c200fa9231))


### Bug Fixes

* **config:** fixed small error in config ([d9b1bd7](https://github.com/krantzy-dev/cc_weather_api/commit/d9b1bd7caf593f26c6fbfbb36732131ace78004b))
