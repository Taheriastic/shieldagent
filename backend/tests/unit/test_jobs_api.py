"""
Tests for jobs API endpoints.
"""

import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
class TestCreateJob:
    """Tests for job creation endpoint."""

    async def test_create_job_success(
        self, client: AsyncClient, auth_headers: dict, test_document
    ):
        """Creating a job with valid documents should succeed."""
        response = await client.post(
            "/api/jobs/evidence-run",
            json={
                "framework": "soc2",
                "document_ids": [str(test_document.id)],
            },
            headers=auth_headers,
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["job_type"] == "soc2"
        assert data["status"] in ["PENDING", "RUNNING"]
        assert data["progress"] >= 0

    async def test_create_job_invalid_document(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Creating a job with non-existent document should fail."""
        fake_id = str(uuid4())
        
        response = await client.post(
            "/api/jobs/evidence-run",
            json={
                "framework": "soc2",
                "document_ids": [fake_id],
            },
            headers=auth_headers,
        )
        
        assert response.status_code == 400
        assert "not found" in response.json()["detail"].lower()

    async def test_create_job_empty_documents(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Creating a job with empty document list should fail."""
        response = await client.post(
            "/api/jobs/evidence-run",
            json={
                "framework": "soc2",
                "document_ids": [],
            },
            headers=auth_headers,
        )
        
        # Should either fail validation or be handled gracefully
        assert response.status_code in [400, 422]

    async def test_create_job_without_auth(self, client: AsyncClient):
        """Creating a job without auth should fail."""
        response = await client.post(
            "/api/jobs/evidence-run",
            json={
                "framework": "soc2",
                "document_ids": [str(uuid4())],
            },
        )
        
        assert response.status_code == 401


@pytest.mark.asyncio
class TestListJobs:
    """Tests for job listing endpoint."""

    async def test_list_jobs_empty(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Empty job list should return properly."""
        response = await client.get(
            "/api/jobs",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "jobs" in data
        assert "total" in data

    async def test_list_jobs_with_items(
        self, client: AsyncClient, auth_headers: dict, test_job
    ):
        """Job list should include existing jobs."""
        response = await client.get(
            "/api/jobs",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    async def test_list_jobs_pagination(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Pagination should work correctly."""
        response = await client.get(
            "/api/jobs?skip=0&limit=5",
            headers=auth_headers,
        )
        
        assert response.status_code == 200


@pytest.mark.asyncio
class TestGetJob:
    """Tests for getting individual jobs."""

    async def test_get_job_success(
        self, client: AsyncClient, auth_headers: dict, test_job
    ):
        """Getting existing job should succeed."""
        response = await client.get(
            f"/api/jobs/{test_job.id}",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_job.id)
        assert "status" in data
        assert "progress" in data

    async def test_get_job_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Getting non-existent job should return 404."""
        fake_id = uuid4()
        
        response = await client.get(
            f"/api/jobs/{fake_id}",
            headers=auth_headers,
        )
        
        assert response.status_code == 404


@pytest.mark.asyncio
class TestJobEvidence:
    """Tests for job evidence endpoint."""

    async def test_get_evidence_success(
        self, client: AsyncClient, auth_headers: dict, test_job
    ):
        """Getting evidence for existing job should succeed."""
        response = await client.get(
            f"/api/jobs/{test_job.id}/evidence",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "evidence_items" in data
        assert "total" in data

    async def test_get_evidence_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Getting evidence for non-existent job should return 404."""
        fake_id = uuid4()
        
        response = await client.get(
            f"/api/jobs/{fake_id}/evidence",
            headers=auth_headers,
        )
        
        assert response.status_code == 404


@pytest.mark.asyncio
class TestJobGaps:
    """Tests for job gaps endpoint."""

    async def test_get_gaps_success(
        self, client: AsyncClient, auth_headers: dict, test_job
    ):
        """Getting gaps for existing job should succeed."""
        response = await client.get(
            f"/api/jobs/{test_job.id}/gaps",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "gaps" in data
        assert "total" in data

    async def test_get_gaps_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Getting gaps for non-existent job should return 404."""
        fake_id = uuid4()
        
        response = await client.get(
            f"/api/jobs/{fake_id}/gaps",
            headers=auth_headers,
        )
        
        assert response.status_code == 404
