import uvicorn

from src.config import settings
from src.logging_config import setup_logging

setup_logging()

app = "src.app:app"


def main() -> None:
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    main()
