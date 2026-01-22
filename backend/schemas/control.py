"""
Control-related Pydantic schemas for request/response validation.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ControlResponse(BaseModel):
    """Schema for control response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    control_id: str
    framework: str
    title: str
    description: str
    check_type: str
    category: str
    required_file_types: str | None


class ControlListResponse(BaseModel):
    """Schema for list of controls response."""

    controls: list[ControlResponse]
    total: int
