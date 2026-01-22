"""
Evidence and Gap Pydantic schemas for request/response validation.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EvidenceItemResponse(BaseModel):
    """Schema for evidence item response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    job_id: UUID
    control_id: str
    status: str
    confidence: float
    summary: str | None
    evidence_quote: str | None
    source_location: str | None
    source_document_ids: list[UUID] | None
    evidence_metadata: dict | None
    created_at: datetime


class EvidenceListResponse(BaseModel):
    """Schema for list of evidence items response."""

    evidence_items: list[EvidenceItemResponse]
    total: int
    passing: int
    failing: int
    needs_review: int


class GapResponse(BaseModel):
    """Schema for gap response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    job_id: UUID
    control_id: str
    severity: str
    description: str
    remediation_suggestion: str | None
    created_at: datetime


class GapListResponse(BaseModel):
    """Schema for list of gaps response."""

    gaps: list[GapResponse]
    total: int
    by_severity: dict[str, int]
