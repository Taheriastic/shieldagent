"""
Tests for document management API endpoints.
"""

import pytest
from httpx import AsyncClient
from io import BytesIO
import json


@pytest.mark.asyncio
class TestDocumentUpload:
    """Tests for document upload endpoint."""

    async def test_upload_json_document(
        self, client: AsyncClient, auth_headers: dict
    ):
        """JSON document upload should succeed."""
        content = json.dumps({"test": "data", "nested": {"key": "value"}})
        files = {
            "file": ("test_policy.json", BytesIO(content.encode()), "application/json")
        }
        
        response = await client.post(
            "/api/documents/upload",
            files=files,
            headers=auth_headers,
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["original_filename"] == "test_policy.json"
        assert data["file_type"] == "json"
        assert data["file_size"] > 0
        assert "id" in data

    async def test_upload_csv_document(
        self, client: AsyncClient, auth_headers: dict
    ):
        """CSV document upload should succeed."""
        content = "name,email,role\nJohn,john@test.com,admin\nJane,jane@test.com,user"
        files = {
            "file": ("users.csv", BytesIO(content.encode()), "text/csv")
        }
        
        response = await client.post(
            "/api/documents/upload",
            files=files,
            headers=auth_headers,
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["file_type"] == "csv"

    async def test_upload_text_document(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Text document upload should succeed."""
        content = "# Security Policy\n\nThis is a test policy document."
        files = {
            "file": ("policy.txt", BytesIO(content.encode()), "text/plain")
        }
        
        response = await client.post(
            "/api/documents/upload",
            files=files,
            headers=auth_headers,
        )
        
        assert response.status_code == 201

    async def test_upload_without_auth(self, client: AsyncClient):
        """Upload without authentication should fail."""
        content = json.dumps({"test": "data"})
        files = {
            "file": ("test.json", BytesIO(content.encode()), "application/json")
        }
        
        response = await client.post("/api/documents/upload", files=files)
        
        assert response.status_code == 401

    async def test_upload_empty_file(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Empty file upload should be handled."""
        files = {
            "file": ("empty.json", BytesIO(b""), "application/json")
        }
        
        response = await client.post(
            "/api/documents/upload",
            files=files,
            headers=auth_headers,
        )
        
        # Should either succeed with 0 bytes or fail with validation error
        assert response.status_code in [201, 400]


@pytest.mark.asyncio
class TestDocumentList:
    """Tests for document listing endpoint."""

    async def test_list_documents_empty(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Empty document list should return properly."""
        response = await client.get(
            "/api/documents",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "documents" in data
        assert "total" in data
        assert isinstance(data["documents"], list)

    async def test_list_documents_with_items(
        self, client: AsyncClient, auth_headers: dict, test_document
    ):
        """Document list should include uploaded documents."""
        response = await client.get(
            "/api/documents",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert len(data["documents"]) >= 1

    async def test_list_documents_pagination(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Pagination parameters should work."""
        response = await client.get(
            "/api/documents?skip=0&limit=10",
            headers=auth_headers,
        )
        
        assert response.status_code == 200

    async def test_list_documents_without_auth(self, client: AsyncClient):
        """Listing documents without auth should fail."""
        response = await client.get("/api/documents")
        
        assert response.status_code == 401


@pytest.mark.asyncio
class TestDocumentGet:
    """Tests for getting individual documents."""

    async def test_get_document_success(
        self, client: AsyncClient, auth_headers: dict, test_document
    ):
        """Getting existing document should succeed."""
        response = await client.get(
            f"/api/documents/{test_document.id}",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_document.id)
        assert data["original_filename"] == test_document.original_filename

    async def test_get_document_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Getting non-existent document should return 404."""
        from uuid import uuid4
        fake_id = uuid4()
        
        response = await client.get(
            f"/api/documents/{fake_id}",
            headers=auth_headers,
        )
        
        assert response.status_code == 404

    async def test_get_document_invalid_uuid(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Invalid UUID should return validation error."""
        response = await client.get(
            "/api/documents/not-a-uuid",
            headers=auth_headers,
        )
        
        assert response.status_code == 422


@pytest.mark.asyncio
class TestDocumentDelete:
    """Tests for document deletion."""

    async def test_delete_document_success(
        self, client: AsyncClient, auth_headers: dict, test_document
    ):
        """Deleting existing document should succeed."""
        response = await client.delete(
            f"/api/documents/{test_document.id}",
            headers=auth_headers,
        )
        
        assert response.status_code == 204

    async def test_delete_document_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Deleting non-existent document should return 404."""
        from uuid import uuid4
        fake_id = uuid4()
        
        response = await client.delete(
            f"/api/documents/{fake_id}",
            headers=auth_headers,
        )
        
        assert response.status_code == 404

    async def test_delete_document_without_auth(
        self, client: AsyncClient, test_document
    ):
        """Deleting without auth should fail."""
        response = await client.delete(
            f"/api/documents/{test_document.id}",
        )
        
        assert response.status_code == 401
