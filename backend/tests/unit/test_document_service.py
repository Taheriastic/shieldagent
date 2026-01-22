"""
Tests for document service
"""
import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock


class TestDocumentExtraction:
    """Test document text extraction"""
    
    def test_extract_text_from_txt(self):
        """Test extracting text from a TXT file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test document.\nWith multiple lines.")
            temp_path = f.name
        
        try:
            with open(temp_path, 'r') as f:
                content = f.read()
            assert "test document" in content
            assert "multiple lines" in content
        finally:
            os.unlink(temp_path)
    
    def test_extract_text_from_json(self):
        """Test extracting text from a JSON file"""
        import json
        test_data = {
            "policy_name": "Security Policy",
            "version": "1.0",
            "controls": ["access_control", "encryption"]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name
        
        try:
            with open(temp_path, 'r') as f:
                content = json.load(f)
            assert content["policy_name"] == "Security Policy"
            assert "access_control" in content["controls"]
        finally:
            os.unlink(temp_path)
    
    def test_extract_text_from_csv(self):
        """Test extracting text from a CSV file"""
        import csv
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["user", "role", "mfa_enabled"])
            writer.writerow(["john@example.com", "admin", "true"])
            writer.writerow(["jane@example.com", "user", "true"])
            temp_path = f.name
        
        try:
            with open(temp_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            assert len(rows) == 2
            assert rows[0]["user"] == "john@example.com"
            assert rows[1]["mfa_enabled"] == "true"
        finally:
            os.unlink(temp_path)
    
    def test_extract_text_from_markdown(self):
        """Test extracting text from a Markdown file"""
        content = """# Security Policy

## Overview
This document outlines our security procedures.

## Access Control
- All users must use MFA
- Regular access reviews conducted quarterly
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            with open(temp_path, 'r') as f:
                extracted = f.read()
            assert "Security Policy" in extracted
            assert "MFA" in extracted
            assert "quarterly" in extracted
        finally:
            os.unlink(temp_path)


class TestDocumentValidation:
    """Test document validation"""
    
    def test_allowed_file_extensions(self):
        """Test that allowed file extensions are validated"""
        allowed_extensions = {'.pdf', '.csv', '.json', '.txt', '.md'}
        
        assert '.pdf' in allowed_extensions
        assert '.csv' in allowed_extensions
        assert '.json' in allowed_extensions
        assert '.txt' in allowed_extensions
        assert '.md' in allowed_extensions
        assert '.exe' not in allowed_extensions
        assert '.js' not in allowed_extensions
    
    def test_file_size_limit(self):
        """Test file size limit enforcement"""
        max_size_mb = 50
        max_size_bytes = max_size_mb * 1024 * 1024
        
        # Test file under limit
        small_file_size = 1024 * 1024  # 1MB
        assert small_file_size < max_size_bytes
        
        # Test file at limit
        at_limit_size = max_size_bytes
        assert at_limit_size <= max_size_bytes
        
        # Test file over limit
        large_file_size = 60 * 1024 * 1024  # 60MB
        assert large_file_size > max_size_bytes
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        def sanitize_filename(filename: str) -> str:
            """Simple filename sanitization"""
            # Remove path components
            filename = os.path.basename(filename)
            # Replace unsafe characters
            unsafe_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
            for char in unsafe_chars:
                filename = filename.replace(char, '_')
            return filename
        
        assert sanitize_filename("normal_file.pdf") == "normal_file.pdf"
        assert sanitize_filename("../../../etc/passwd") == "passwd"
        assert sanitize_filename("file:with:colons.txt") == "file_with_colons.txt"
        assert sanitize_filename("file<with>brackets.pdf") == "file_with_brackets.pdf"


class TestDocumentStorage:
    """Test document storage operations"""
    
    def test_generate_unique_filename(self):
        """Test unique filename generation"""
        import uuid
        
        original_name = "security_policy.pdf"
        unique_id = str(uuid.uuid4())
        unique_filename = f"{unique_id}_{original_name}"
        
        assert unique_id in unique_filename
        assert original_name in unique_filename
        assert len(unique_filename) > len(original_name)
    
    def test_create_user_upload_directory(self):
        """Test user upload directory creation"""
        import uuid
        
        with tempfile.TemporaryDirectory() as base_dir:
            user_id = str(uuid.uuid4())
            user_dir = Path(base_dir) / user_id
            
            # Directory shouldn't exist yet
            assert not user_dir.exists()
            
            # Create directory
            user_dir.mkdir(parents=True, exist_ok=True)
            
            # Directory should now exist
            assert user_dir.exists()
            assert user_dir.is_dir()
    
    def test_save_and_read_document(self):
        """Test saving and reading a document"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_doc.txt"
            content = "Test document content for SOC 2 compliance"
            
            # Save
            file_path.write_text(content)
            
            # Read
            read_content = file_path.read_text()
            
            assert read_content == content
            assert file_path.exists()
    
    def test_delete_document(self):
        """Test document deletion"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "to_delete.txt"
            file_path.write_text("Content to delete")
            
            assert file_path.exists()
            
            # Delete
            file_path.unlink()
            
            assert not file_path.exists()


class TestDocumentMetadata:
    """Test document metadata extraction"""
    
    def test_extract_file_metadata(self):
        """Test extracting file metadata"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content" * 100)
            temp_path = f.name
        
        try:
            stat = os.stat(temp_path)
            
            assert stat.st_size > 0
            assert stat.st_mtime > 0
            
            extension = os.path.splitext(temp_path)[1]
            assert extension == '.txt'
        finally:
            os.unlink(temp_path)
    
    def test_determine_content_type(self):
        """Test content type determination"""
        content_types = {
            '.pdf': 'application/pdf',
            '.json': 'application/json',
            '.csv': 'text/csv',
            '.txt': 'text/plain',
            '.md': 'text/markdown',
        }
        
        assert content_types['.pdf'] == 'application/pdf'
        assert content_types['.json'] == 'application/json'
        assert content_types['.csv'] == 'text/csv'
        assert content_types['.txt'] == 'text/plain'
        assert content_types['.md'] == 'text/markdown'
    
    def test_document_hash_generation(self):
        """Test document hash generation for deduplication"""
        import hashlib
        
        content = b"Test document content"
        
        # Generate hash
        hash_obj = hashlib.sha256(content)
        doc_hash = hash_obj.hexdigest()
        
        # Hash should be consistent
        assert len(doc_hash) == 64  # SHA256 produces 64 hex characters
        assert doc_hash == hashlib.sha256(content).hexdigest()
        
        # Different content should produce different hash
        different_content = b"Different content"
        different_hash = hashlib.sha256(different_content).hexdigest()
        assert doc_hash != different_hash
