from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.health import health_router
from backend.app.core.config import Settings
from backend.app.api.companies import router as company_router
from backend.app.api.rooms import router as room_router
from backend.app.api.body_limit import BodyLimitMiddleware


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    @asynccontextmanager
    async def lifespan(application):
        yield
        if application.state.engine is not None:
            application.state.engine.dispose()

    application = FastAPI(
        title=settings.project_name,
        version=settings.version,
        description="VAULT internal profiles and local synthetic data rooms. No buyer disclosure or authentication is implemented.",
        lifespan=lifespan,
    )
    application.state.settings = settings
    application.state.engine = None
    application.state.session_factory = None
    allowed_origins = sorted(settings.allowed_origin_values())
    if allowed_origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_methods=["GET", "POST", "PUT", "OPTIONS"],
            allow_headers=["Accept", "Content-Type", "X-Demo-Password"],
            expose_headers=["Content-Disposition"],
            max_age=600,
        )
    application.add_middleware(BodyLimitMiddleware, max_bytes=settings.max_upload_bytes + 65536)
    application.include_router(health_router(settings), prefix=settings.api_v1_str)
    application.include_router(company_router, prefix=settings.api_v1_str)
    application.include_router(room_router, prefix=settings.api_v1_str)
    return application


app = create_app()
