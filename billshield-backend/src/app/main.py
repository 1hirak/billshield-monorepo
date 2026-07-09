from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.errors import AppError
from app.core.logging import get_logger, setup_logging
from app.db.init_db import init_db
from app.routers import (
    bills,
    dashboard,
    dev,
    health,
    households,
    plans,
    recommendations,
    scenarios,
    support_services,
)

logger = get_logger(__name__)


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_prefix = settings.API_PREFIX

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        logger.warning(f"AppError: {exc.code} - {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": "HTTP_ERROR",
                    "message": str(exc.detail),
                    "details": {},
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled error: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Something went wrong. Please try again later.",
                    "details": {},
                }
            },
        )

    app.include_router(health.router, prefix=api_prefix)
    app.include_router(households.router, prefix=api_prefix)
    app.include_router(bills.router, prefix=api_prefix)
    app.include_router(dashboard.router, prefix=api_prefix)
    app.include_router(scenarios.router, prefix=api_prefix)
    app.include_router(support_services.router, prefix=api_prefix)
    app.include_router(plans.router, prefix=api_prefix)
    app.include_router(recommendations.router, prefix=api_prefix)
    app.include_router(dev.router, prefix=api_prefix)

    @app.on_event("startup")
    def on_startup():
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        init_db()
        logger.info(f"BillShield UK API started in {settings.APP_ENV} mode.")

    return app


app = create_app()
