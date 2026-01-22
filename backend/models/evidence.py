"""
Evidence and Gap models for compliance analysis results.
"""

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import String, DateTime, Float, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class EvidenceStatus(str, Enum):
    """Status of evidence item evaluation."""
    PASS = "pass"
    FAIL = "fail"
    NEEDS_REVIEW = "needs_review"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"


class GapSeverity(str, Enum):
    """Severity level of compliance gaps."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EvidenceItem(Base):
    """Evidence item generated from compliance control check."""

    __tablename__ = "evidence_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    control_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=EvidenceStatus.NEEDS_REVIEW.value,
    )
    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    evidence_quote: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    source_location: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    raw_llm_response: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    source_document_ids: Mapped[list[uuid.UUID] | None] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        nullable=True,
    )
    evidence_metadata: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    job: Mapped["Job"] = relationship(
        "Job",
        back_populates="evidence_items",
    )

    def __repr__(self) -> str:
        return (
            f"<EvidenceItem(id={self.id}, "
            f"control_id={self.control_id}, status={self.status})>"
        )


class Gap(Base):
    """Compliance gap identified during analysis."""

    __tablename__ = "gaps"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    control_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=GapSeverity.MEDIUM.value,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    remediation_suggestion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    job: Mapped["Job"] = relationship(
        "Job",
        back_populates="gaps",
    )

    def __repr__(self) -> str:
        return (
            f"<Gap(id={self.id}, "
            f"control_id={self.control_id}, severity={self.severity})>"
        )
