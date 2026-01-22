"""
Integration tests for the Gemini service.
These tests are marked to skip when API key is not available.
"""

import pytest
import os

from services.gemini_service import GeminiService


# Skip all tests if no API key
pytestmark = pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY") or 
    os.environ.get("GEMINI_API_KEY") == "test-api-key",
    reason="GEMINI_API_KEY not configured for integration tests"
)


class TestGeminiServiceInit:
    """Tests for Gemini service initialization."""

    def test_init_quick_scan(self):
        """Quick scan initialization should load 8 controls."""
        service = GeminiService(scan_type="quick")
        assert len(service.controls) == 8

    def test_init_full_scan(self):
        """Full scan initialization should load 50+ controls."""
        service = GeminiService(scan_type="full")
        assert len(service.controls) >= 50

    def test_get_controls(self):
        """get_controls should return control list."""
        service = GeminiService()
        controls = service.get_controls()
        
        assert isinstance(controls, list)
        assert len(controls) > 0

    def test_get_all_available_controls(self):
        """get_all_available_controls should return full list."""
        service = GeminiService(scan_type="quick")
        all_controls = service.get_all_available_controls()
        
        assert len(all_controls) >= 50

    def test_get_control_stats(self):
        """get_control_stats should return summary."""
        service = GeminiService()
        stats = service.get_control_stats()
        
        assert "total_controls" in stats
        assert "categories" in stats


class TestDocumentExtraction:
    """Tests for document text extraction."""

    @pytest.mark.asyncio
    async def test_extract_json_text(self, tmp_path):
        """JSON extraction should work."""
        service = GeminiService()
        
        # Create test JSON file
        json_file = tmp_path / "test.json"
        json_file.write_text('{"key": "value", "nested": {"a": 1}}')
        
        text = await service.extract_document_text(str(json_file))
        
        assert "key" in text
        assert "value" in text

    @pytest.mark.asyncio
    async def test_extract_csv_text(self, tmp_path):
        """CSV extraction should work."""
        service = GeminiService()
        
        # Create test CSV file
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,email\nJohn,john@test.com")
        
        text = await service.extract_document_text(str(csv_file))
        
        assert "name" in text
        assert "John" in text

    @pytest.mark.asyncio
    async def test_extract_txt_text(self, tmp_path):
        """Text file extraction should work."""
        service = GeminiService()
        
        # Create test text file
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("This is a test document content.")
        
        text = await service.extract_document_text(str(txt_file))
        
        assert "test document" in text

    @pytest.mark.asyncio
    async def test_extract_nonexistent_file(self):
        """Non-existent file should raise error."""
        service = GeminiService()
        
        with pytest.raises(FileNotFoundError):
            await service.extract_document_text("/nonexistent/file.json")


class TestJsonParsing:
    """Tests for JSON response parsing."""

    def test_parse_valid_json(self):
        """Valid JSON should parse correctly."""
        service = GeminiService()
        
        response = '{"status": "pass", "confidence": 0.9}'
        result = service._parse_json_response(response)
        
        assert result["status"] == "pass"
        assert result["confidence"] == 0.9

    def test_parse_json_in_markdown(self):
        """JSON in markdown code block should parse."""
        service = GeminiService()
        
        response = '''```json
{"status": "fail", "confidence": 0.5}
```'''
        result = service._parse_json_response(response)
        
        assert result["status"] == "fail"

    def test_parse_invalid_json(self):
        """Invalid JSON should return default structure."""
        service = GeminiService()
        
        response = "This is not JSON at all"
        result = service._parse_json_response(response)
        
        assert result["status"] == "needs_review"
        assert result["confidence"] == 0.0


class TestRemediation:
    """Tests for remediation suggestion generation."""

    def test_get_remediation_known_control(self):
        """Known control should return specific remediation."""
        service = GeminiService()
        
        remediation = service._get_remediation("CC6.1", "Missing MFA")
        
        assert len(remediation) > 20
        assert "implement" in remediation.lower() or "mfa" in remediation.lower()

    def test_get_remediation_unknown_control(self):
        """Unknown control should return generic remediation."""
        service = GeminiService()
        
        remediation = service._get_remediation("UNKNOWN", "Some gap")
        
        assert len(remediation) > 10
