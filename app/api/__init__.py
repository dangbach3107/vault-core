from fastapi import APIRouter
from .profile_routes import router as profile_router
from .vdr_routes import router as vdr_router
from .approval_routes import router as approval_router
from .techdd_routes import router as techdd_router

api_router = APIRouter()
api_router.include_router(profile_router)
api_router.include_router(vdr_router)
api_router.include_router(approval_router)
api_router.include_router(techdd_router)
