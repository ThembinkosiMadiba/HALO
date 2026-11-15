r"""Start the HALO API for local development, bound to a loopback address only.

Run from the repository root:
    backend\.venv\Scripts\python.exe backend\run_dev.py
"""
import uvicorn

from app.core.config import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
