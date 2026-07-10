import logging.config

from src.config import settings


def setup_logging() -> None:
    """Configure the root logger using the level resolved in Settings."""
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": settings.effective_log_level,
            "handlers": ["console"],
        },
        "loggers": {
            "uvicorn.access": {"level": "WARNING", "propagate": True},
        },
    }

    logging.config.dictConfig(config)
