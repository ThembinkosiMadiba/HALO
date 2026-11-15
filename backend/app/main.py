"""HALO API application factory."""
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.health import router as health_router
from app.core.config import Settings, get_settings
from app.core.logging_config import LOGGER_NAME, configure_logging


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings)

    docs = settings.docs_enabled
    app = FastAPI(
        title="HALO",
        docs_url="/docs" if docs else None,
        redoc_url="/redoc" if docs else None,
        openapi_url="/openapi.json" if docs else None,
    )

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(Exception)
    async def unhandled_error(request: Request, exc: Exception) -> JSONResponse:
        # Log only the error type: messages can contain sensitive values.
        logging.getLogger(LOGGER_NAME).error(
            "Unhandled error on %s %s: %s", request.method, request.url.path, type(exc).__name__
        )
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    app.include_router(health_router, prefix="/api/v1")
    return app


app = create_app()
