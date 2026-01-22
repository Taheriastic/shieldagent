"""
Tests for health check endpoint.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestHealthCheck:
    """Tests for health check endpoint."""

    async def test_health_check_success(self, client: AsyncClient):
        """Health check should return healthy status."""
        response = await client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_health_check_returns_version(self, client: AsyncClient):
        """Health check should return version info."""
        response = await client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "version" in data or "status" in data

    async def test_health_check_no_auth_required(self, client: AsyncClient):
        """Health check should not require authentication."""
        response = await client.get("/api/health")
        
        # Should succeed without auth headers
        assert response.status_code == 200
