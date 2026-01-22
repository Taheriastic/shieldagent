"""
Job management API endpoints for compliance analysis.
"""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from core.dependencies import DbSession, CurrentUserId
from schemas.job import JobCreate, JobResponse, JobListResponse
from schemas.evidence import EvidenceListResponse, GapListResponse
from services.job_service import JobService
from services.document_service import DocumentService
from models.job import Job, JobStatus
from models.document import Document
from models.evidence import EvidenceItem, Gap, EvidenceStatus, GapSeverity

router = APIRouter()


@router.post(
    "/evidence-run",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_evidence_run(
    job_data: JobCreate,
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> JobResponse:
    """
    Create a new compliance evidence collection job.
    
    This will start an async job that analyzes the provided documents
    against SOC 2 compliance controls.
    
    Args:
        job_data: Job creation data including document_ids and scan_type
            - scan_type: "quick" for 8 key controls, "full" for all 51
    """
    user_uuid = UUID(user_id)
    
    # Verify all documents exist and belong to user
    doc_service = DocumentService(db)
    documents = await doc_service.get_documents_by_ids(
        document_ids=job_data.document_ids,
        user_id=user_uuid,
    )
    
    if len(documents) != len(job_data.document_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more documents not found",
        )
    
    # Create job with scan_type
    job_service = JobService(db)
    job = await job_service.create_job(
        job_data=job_data,
        user_id=user_uuid,
    )
    
    # Try to enqueue Celery task for async processing
    try:
        from worker.tasks import run_compliance_analysis
        task = run_compliance_analysis.delay(
            str(job.id),
            [str(d) for d in job_data.document_ids],
            job_data.scan_type,
        )
        # Update job with celery task ID
        job.celery_task_id = task.id
        await db.commit()
        await db.refresh(job)
    except Exception as e:
        # Celery not available - job will stay pending
        print(f"Celery not available: {e}")
    
    return JobResponse.model_validate(job)


@router.get("", response_model=JobListResponse)
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> JobListResponse:
    """List all jobs for the authenticated user."""
    service = JobService(db)
    return await service.list_jobs(
        user_id=UUID(user_id),
        skip=skip,
        limit=limit,
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: UUID,
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> JobResponse:
    """Get a specific job by ID."""
    service = JobService(db)
    job = await service.get_job(
        job_id=job_id,
        user_id=UUID(user_id),
    )
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    return JobResponse.model_validate(job)


@router.get("/{job_id}/evidence", response_model=EvidenceListResponse)
async def get_job_evidence(
    job_id: UUID,
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> EvidenceListResponse:
    """Get all evidence items for a job."""
    service = JobService(db)
    result = await service.get_job_evidence(
        job_id=job_id,
        user_id=UUID(user_id),
    )
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    return result


@router.get("/{job_id}/gaps", response_model=GapListResponse)
async def get_job_gaps(
    job_id: UUID,
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> GapListResponse:
    """Get all compliance gaps for a job."""
    service = JobService(db)
    result = await service.get_job_gaps(
        job_id=job_id,
        user_id=UUID(user_id),
    )
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    return result


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: UUID,
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> None:
    """Delete a job and all related data."""
    service = JobService(db)
    deleted = await service.delete_job(
        job_id=job_id,
        user_id=UUID(user_id),
    )
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )


@router.post(
    "/{job_id}/run",
    response_model=JobResponse,
)
async def run_job_analysis(
    job_id: UUID,
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> JobResponse:
    """
    Run compliance analysis for a job.
    
    This runs the Gemini AI analysis directly.
    Use this when Celery worker is not available.
    """
    from services.gemini_service import get_gemini_service
    
    service = JobService(db)
    job = await service.get_job(job_id=job_id, user_id=UUID(user_id))
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    if job.status not in [JobStatus.PENDING.value, JobStatus.FAILED.value]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job cannot be run in {job.status} status",
        )
    
    # Get user's documents
    result = await db.execute(
        select(Document).where(Document.user_id == UUID(user_id))
    )
    documents = result.scalars().all()
    
    if not documents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No documents found for analysis",
        )
    
    # Update job to running
    job.status = JobStatus.RUNNING.value
    job.started_at = datetime.now(timezone.utc)
    job.error_message = None
    await db.commit()
    
    try:
        # Get document file paths
        doc_paths = [doc.file_path for doc in documents]
        doc_ids = [doc.id for doc in documents]
        
        # Get scan_type from job (default to quick)
        scan_type = getattr(job, 'scan_type', 'quick') or 'quick'
        
        # Initialize Gemini service with scan_type and run analysis
        gemini = get_gemini_service(scan_type=scan_type)
        
        # Update total controls based on scan type
        job.total_controls = len(gemini.get_controls())
        await db.commit()
        
        analysis_results = await gemini.analyze_documents(doc_paths)
        
        # Save evidence items
        for evidence_data in analysis_results["evidence_items"]:
            status_map = {
                "pass": EvidenceStatus.PASS.value,
                "fail": EvidenceStatus.FAIL.value,
                "needs_review": EvidenceStatus.NEEDS_REVIEW.value,
                "error": EvidenceStatus.ERROR.value,
            }
            
            evidence = EvidenceItem(
                job_id=job_id,
                control_id=evidence_data["control_id"],
                status=status_map.get(
                    evidence_data.get("status", "needs_review"),
                    EvidenceStatus.NEEDS_REVIEW.value
                ),
                confidence=evidence_data.get("confidence", 0.0),
                summary=evidence_data.get("summary", ""),
                evidence_quote=evidence_data.get("evidence_quote"),
                raw_llm_response={
                    "response": evidence_data.get("raw_llm_response")
                },
                source_document_ids=list(doc_ids),
            )
            db.add(evidence)
        
        # Save gaps
        for gap_data in analysis_results.get("gaps", []):
            severity_map = {
                "critical": GapSeverity.CRITICAL.value,
                "high": GapSeverity.HIGH.value,
                "medium": GapSeverity.MEDIUM.value,
                "low": GapSeverity.LOW.value,
            }
            
            gap = Gap(
                job_id=job_id,
                control_id=gap_data["control_id"],
                severity=severity_map.get(
                    gap_data.get("severity", "medium"),
                    GapSeverity.MEDIUM.value
                ),
                description=gap_data["description"],
                remediation_suggestion=gap_data.get("remediation_suggestion"),
            )
            db.add(gap)
        
        # Update job as completed
        job.status = JobStatus.SUCCEEDED.value
        job.progress = 100
        job.completed_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(job)
        
    except Exception as e:
        # Update job as failed
        job.status = JobStatus.FAILED.value
        job.error_message = str(e)
        job.completed_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(job)
    
    return JobResponse.model_validate(job)
