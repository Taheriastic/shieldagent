"""
Document-related Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DocumentCreate(BaseModel):
    """Schema for document creation (internal use)."""

    filename: str
    original_filename: str
    file_type: str
    file_path: str
    file_size: int
    content_hash: str | None = None
    metadata: dict | None = None


class DocumentResponse(BaseModel):
    """Schema for document response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    uploaded_at: datetime
    metadata: dict | None = Field(default=None, validation_alias="metadata_")
    
    @field_validator("metadata", mode="before")
    @classmethod
    def convert_metadata(cls, v: Any) -> dict | None:
        """Convert metadata to dict if needed."""
        if v is None:
            return None
        if isinstance(v, dict):
            return v
        # Handle SQLAlchemy MetaData or other objects
        return {}


class DocumentListResponse(BaseModel):
    """Schema for list of documents response."""

    documents: list[DocumentResponse]
    total: int
