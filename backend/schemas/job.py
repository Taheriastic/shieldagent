"""
Job-related Pydantic schemas for request/response validation.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    """Schema for job creation request."""

    framework: str = Field(
        default="soc2_lite",
        description="Compliance framework to check against",
    )
    document_ids: list[UUID] = Field(
        ...,
        min_length=1,
        description="List of document IDs to analyze",
    )


class JobResponse(BaseModel):
    """Schema for job response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    job_type: str
    status: str
    progress: int
    total_controls: int
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime


class JobListResponse(BaseModel):
    """Schema for list of jobs response."""

    jobs: list[JobResponse]
    total: int


class JobStatusUpdate(BaseModel):
    """Schema for job status update (internal use)."""

    status: str
    progress: int | None = None
    error_message: str | None = None
