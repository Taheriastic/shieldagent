"""
Job service for compliance analysis job management.
"""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.job import Job, JobStatus
from models.evidence import EvidenceItem, Gap, EvidenceStatus, GapSeverity
from schemas.job import JobCreate, JobResponse, JobListResponse
from schemas.evidence import (
    EvidenceListResponse,
    EvidenceItemResponse,
    GapListResponse,
    GapResponse,
)


class JobService:
    """Service class for job-related operations."""

    def __init__(self, db: AsyncSession) -> None:
        """
        Initialize the job service.

        Args:
            db: Async database session.
        """
        self.db = db

    async def create_job(
        self,
        job_data: JobCreate,
        user_id: UUID,
    ) -> Job:
        """
        Create a new compliance analysis job.

        Args:
            job_data: The job creation data.
            user_id: The ID of the user creating the job.

        Returns:
            The created Job object.
        """
        job = Job(
            user_id=user_id,
            job_type=job_data.framework,
            status=JobStatus.PENDING.value,
            progress=0,
            total_controls=8,
        )

        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)

        return job

    async def get_job(
        self,
        job_id: UUID,
        user_id: UUID,
    ) -> Job | None:
        """
        Get a job by ID for a specific user.

        Args:
            job_id: The job UUID.
            user_id: The user's UUID.

        Returns:
            The Job object if found and owned by user, None otherwise.
        """
        result = await self.db.execute(
            select(Job).where(
                Job.id == job_id,
                Job.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_jobs(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> JobListResponse:
        """
        List all jobs for a user.

        Args:
            user_id: The user's UUID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            JobListResponse with jobs and total count.
        """
        # Get total count
        count_result = await self.db.execute(
            select(func.count()).select_from(Job).where(
                Job.user_id == user_id
            )
        )
        total = count_result.scalar_one()

        # Get jobs
        result = await self.db.execute(
            select(Job)
            .where(Job.user_id == user_id)
            .order_by(Job.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        jobs = result.scalars().all()

        return JobListResponse(
            jobs=[JobResponse.model_validate(job) for job in jobs],
            total=total,
        )

    async def update_job_status(
        self,
        job_id: UUID,
        status: JobStatus,
        progress: int | None = None,
        error_message: str | None = None,
    ) -> Job | None:
        """
        Update job status and progress.

        Args:
            job_id: The job UUID.
            status: The new status.
            progress: Optional progress value.
            error_message: Optional error message.

        Returns:
            The updated Job object, or None if not found.
        """
        result = await self.db.execute(
            select(Job).where(Job.id == job_id)
        )
        job = result.scalar_one_or_none()

        if not job:
            return None

        job.status = status.value
        if progress is not None:
            job.progress = progress
        if error_message is not None:
            job.error_message = error_message

        if status == JobStatus.RUNNING and job.started_at is None:
            job.started_at = datetime.now(timezone.utc)
        elif status in (JobStatus.SUCCEEDED, JobStatus.FAILED):
            job.completed_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(job)

        return job

    async def get_job_evidence(
        self,
        job_id: UUID,
        user_id: UUID,
    ) -> EvidenceListResponse | None:
        """
        Get all evidence items for a job.

        Args:
            job_id: The job UUID.
            user_id: The user's UUID.

        Returns:
            EvidenceListResponse if job exists, None otherwise.
        """
        # Verify job ownership
        job = await self.get_job(job_id, user_id)
        if not job:
            return None

        # Get evidence items
        result = await self.db.execute(
            select(EvidenceItem)
            .where(EvidenceItem.job_id == job_id)
            .order_by(EvidenceItem.control_id)
        )
        evidence_items = result.scalars().all()

        # Calculate statistics
        passing = sum(
            1 for e in evidence_items
            if e.status == EvidenceStatus.PASS.value
        )
        failing = sum(
            1 for e in evidence_items
            if e.status == EvidenceStatus.FAIL.value
        )
        needs_review = sum(
            1 for e in evidence_items
            if e.status == EvidenceStatus.NEEDS_REVIEW.value
        )

        return EvidenceListResponse(
            evidence_items=[
                EvidenceItemResponse.model_validate(e) for e in evidence_items
            ],
            total=len(evidence_items),
            passing=passing,
            failing=failing,
            needs_review=needs_review,
        )

    async def get_job_gaps(
        self,
        job_id: UUID,
        user_id: UUID,
    ) -> GapListResponse | None:
        """
        Get all gaps for a job.

        Args:
            job_id: The job UUID.
            user_id: The user's UUID.

        Returns:
            GapListResponse if job exists, None otherwise.
        """
        # Verify job ownership
        job = await self.get_job(job_id, user_id)
        if not job:
            return None

        # Get gaps
        result = await self.db.execute(
            select(Gap)
            .where(Gap.job_id == job_id)
            .order_by(Gap.severity, Gap.control_id)
        )
        gaps = result.scalars().all()

        # Calculate severity breakdown
        by_severity = {
            GapSeverity.CRITICAL.value: 0,
            GapSeverity.HIGH.value: 0,
            GapSeverity.MEDIUM.value: 0,
            GapSeverity.LOW.value: 0,
        }
        for gap in gaps:
            if gap.severity in by_severity:
                by_severity[gap.severity] += 1

        return GapListResponse(
            gaps=[GapResponse.model_validate(g) for g in gaps],
            total=len(gaps),
            by_severity=by_severity,
        )

    async def delete_job(
        self,
        job_id: UUID,
        user_id: UUID,
    ) -> bool:
        """
        Delete a job and all related records.

        Args:
            job_id: The job UUID.
            user_id: The user's UUID.

        Returns:
            True if deleted, False if not found.
        """
        job = await self.get_job(job_id, user_id)
        if not job:
            return False

        await self.db.delete(job)
        await self.db.commit()

        return True
