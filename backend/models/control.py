"""
Control model for SOC 2 compliance controls reference data.
"""

import uuid
from enum import Enum

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base, GUID


class CheckType(str, Enum):
    """Type of control check to perform."""
    AI_PROMPT = "ai_prompt"
    DETERMINISTIC = "deterministic"


class Control(Base):
    """SOC 2 compliance control reference data."""

    __tablename__ = "controls"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
    )
    control_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    framework: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="SOC2",
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    check_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    required_file_types: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Control(control_id={self.control_id}, title={self.title})>"
