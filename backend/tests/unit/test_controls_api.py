"""
Tests for controls API endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestListControls:
    """Tests for controls listing endpoint."""

    async def test_list_controls_default(self, client: AsyncClient):
        """Default control listing should return quick scan controls."""
        response = await client.get("/api/controls")
        
        assert response.status_code == 200
        data = response.json()
        assert "controls" in data
        assert "total" in data
        assert data["total"] == 8  # Quick scan has 8 controls

    async def test_list_controls_full_scan(self, client: AsyncClient):
        """Full scan should return all 50+ controls."""
        response = await client.get("/api/controls?scan_type=full")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 50  # Full scan has 50+ controls

    async def test_list_controls_by_category(self, client: AsyncClient):
        """Filtering by category should work."""
        response = await client.get(
            "/api/controls?scan_type=full&category=Privacy"
        )
        
        assert response.status_code == 200
        data = response.json()
        # All returned controls should be Privacy category
        for control in data["controls"]:
            assert "privacy" in control["category"].lower()

    async def test_control_structure(self, client: AsyncClient):
        """Control response should have correct structure."""
        response = await client.get("/api/controls")
        
        assert response.status_code == 200
        data = response.json()
        
        if data["controls"]:
            control = data["controls"][0]
            assert "id" in control
            assert "control_id" in control
            assert "framework" in control
            assert "title" in control
            assert "description" in control
            assert "category" in control


@pytest.mark.asyncio
class TestControlCategories:
    """Tests for control categories endpoint."""

    async def test_list_categories(self, client: AsyncClient):
        """Categories endpoint should return category list."""
        response = await client.get("/api/controls/categories")
        
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert "total_categories" in data
        assert data["total_categories"] > 0

    async def test_category_structure(self, client: AsyncClient):
        """Category response should have correct structure."""
        response = await client.get("/api/controls/categories")
        
        assert response.status_code == 200
        data = response.json()
        
        if data["categories"]:
            category = data["categories"][0]
            assert "name" in category
            assert "count" in category
            assert "controls" in category


@pytest.mark.asyncio
class TestControlSummary:
    """Tests for control summary endpoint."""

    async def test_get_summary(self, client: AsyncClient):
        """Summary endpoint should return control statistics."""
        response = await client.get("/api/controls/summary")
        
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "quick_scan_count" in data
        assert "full_scan_count" in data
        assert data["quick_scan_count"] == 8
        assert data["full_scan_count"] >= 50


@pytest.mark.asyncio
class TestGetControl:
    """Tests for individual control retrieval."""

    async def test_get_control_success(self, client: AsyncClient):
        """Getting existing control should succeed."""
        response = await client.get("/api/controls/CC6.1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["control_id"] == "CC6.1"
        assert data["framework"] == "SOC2"
        assert "title" in data
        assert "description" in data
        assert "check_prompt" in data

    async def test_get_control_lowercase(self, client: AsyncClient):
        """Control ID should be case-insensitive."""
        response = await client.get("/api/controls/cc6.1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["control_id"] == "CC6.1"

    async def test_get_control_not_found(self, client: AsyncClient):
        """Getting non-existent control should return error."""
        response = await client.get("/api/controls/INVALID")
        
        assert response.status_code == 200  # Returns error in body
        data = response.json()
        assert "error" in data

    async def test_get_availability_control(self, client: AsyncClient):
        """Availability controls should be retrievable."""
        response = await client.get("/api/controls/A1.1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["control_id"] == "A1.1"
        assert "Availability" in data["category"]

    async def test_get_privacy_control(self, client: AsyncClient):
        """Privacy controls should be retrievable."""
        response = await client.get("/api/controls/P1.1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["control_id"] == "P1.1"
        assert "Privacy" in data["category"]
