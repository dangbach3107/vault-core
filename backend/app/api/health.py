from fastapi import APIRouter

from backend.app.core.config import Settings
from backend.app.schemas.health import HealthResponse


def health_router(settings: Settings) -> APIRouter:
    router = APIRouter()

    @router.get(
        "/health",
        response_model=HealthResponse,
        tags=["Health"],
        operation_id="get_health",
        summary="Check that the API is responding",
        description="Liveness only. Does not check PostgreSQL or external providers.",
    )
    def get_health() -> HealthResponse:
        return HealthResponse(
            status="ok",
            service=settings.project_name,
            version=settings.version,
            scope="liveness",
        )

    return router
