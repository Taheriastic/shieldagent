"""API routes package initialization."""

from fastapi import APIRouter

from api.health import router as health_router
from api.auth import router as auth_router
from api.documents import router as documents_router
from api.jobs import router as jobs_router
from api.controls import router as controls_router
from api.reports import router as reports_router
from api.risk import router as risk_router

# Main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(
    documents_router,
    prefix="/documents",
    tags=["Documents"],
)
api_router.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(
    controls_router,
    prefix="/controls",
    tags=["Controls"],
)
api_router.include_router(
    reports_router,
    prefix="/reports",
    tags=["Reports"],
)
api_router.include_router(
    risk_router,
    prefix="/risk",
    tags=["Risk Analysis"],
)

__all__ = ["api_router"]
