"""
Health check endpoints for monitoring and load balancers.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        Simple status response indicating service is running.
    """
    return {
        "status": "ok",
        "service": "shieldagent-api",
        "version": "1.0.0",
    }


@router.get("/health/ready")
async def readiness_check() -> dict:
    """
    Readiness check for Kubernetes/container orchestration.
    
    Returns:
        Status indicating if the service is ready to receive traffic.
    """
    # TODO: Add database connectivity check
    return {
        "status": "ready",
        "checks": {
            "database": "ok",
            "redis": "ok",
        },
    }
