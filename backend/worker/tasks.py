"""
Celery tasks for compliance analysis background processing.
"""

import asyncio
from datetime import datetime, timezone
from uuid import UUID

from celery import current_task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings
from models.job import Job, JobStatus
from models.document import Document
from models.evidence import EvidenceItem, Gap, EvidenceStatus, GapSeverity
from services.gemini_service import get_gemini_service
from worker.celery_app import celery_app


def get_async_session():
    """Create async database session for worker."""
    engine = create_async_engine(settings.database_url, echo=False)
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def _run_analysis(
    job_id: str,
    document_ids: list[str],
    scan_type: str = "quick",
) -> dict:
    """
    Internal async function to run compliance analysis.
    
    Args:
        job_id: The job UUID string.
        document_ids: List of document UUID strings.
        scan_type: "quick" for 8 controls, "full" for all 51.
        
    Returns:
        Analysis results dictionary.
    """
    AsyncSessionLocal = get_async_session()
    
    async with AsyncSessionLocal() as db:
        # Get job
        result = await db.execute(
            select(Job).where(Job.id == UUID(job_id))
        )
        job = result.scalar_one_or_none()
        
        if not job:
            raise ValueError(f"Job not found: {job_id}")
        
        # Update job to running
        job.status = JobStatus.RUNNING.value
        job.started_at = datetime.now(timezone.utc)
        await db.commit()
        
        try:
            # Get documents
            result = await db.execute(
                select(Document).where(
                    Document.id.in_([UUID(d) for d in document_ids])
                )
            )
            documents = result.scalars().all()
            
            if not documents:
                raise ValueError("No documents found for analysis")
            
            # Get document file paths
            doc_paths = [doc.file_path for doc in documents]
            
            # Initialize Gemini service with scan_type
            gemini = get_gemini_service(scan_type=scan_type)
            controls = gemini.get_controls()
            
            # Progress callback
            def update_progress(current, total, control_id):
                progress = int((current / total) * 100)
                # Update task state for Celery
                current_task.update_state(
                    state="PROGRESS",
                    meta={
                        "current": current,
                        "total": total,
                        "control_id": control_id,
                        "progress": progress,
                    }
                )
            
            # Update job total controls
            job.total_controls = len(controls)
            await db.commit()
            
            # Run analysis
            analysis_results = await gemini.analyze_documents(
                doc_paths,
                progress_callback=update_progress,
            )
            
            # Save evidence items
            for evidence_data in analysis_results["evidence_items"]:
                status_map = {
                    "pass": EvidenceStatus.PASS.value,
                    "fail": EvidenceStatus.FAIL.value,
                    "needs_review": EvidenceStatus.NEEDS_REVIEW.value,
                    "error": EvidenceStatus.ERROR.value,
                }
                
                evidence = EvidenceItem(
                    job_id=UUID(job_id),
                    control_id=evidence_data["control_id"],
                    status=status_map.get(
                        evidence_data.get("status", "needs_review"),
                        EvidenceStatus.NEEDS_REVIEW.value
                    ),
                    confidence=evidence_data.get("confidence", 0.0),
                    summary=evidence_data.get("summary", ""),
                    evidence_quote=evidence_data.get("evidence_quote"),
                    raw_llm_response={"response": evidence_data.get("raw_llm_response")},
                    source_document_ids=[UUID(d) for d in document_ids],
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
                    job_id=UUID(job_id),
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
            
            return {
                "status": "success",
                "job_id": job_id,
                "evidence_count": len(analysis_results["evidence_items"]),
                "gap_count": len(analysis_results.get("gaps", [])),
                "summary": analysis_results["summary"],
            }
            
        except Exception as e:
            # Update job as failed
            job.status = JobStatus.FAILED.value
            job.error_message = str(e)
            job.completed_at = datetime.now(timezone.utc)
            await db.commit()
            
            raise


@celery_app.task(bind=True, max_retries=3)
def run_compliance_analysis(
    self,
    job_id: str,
    document_ids: list[str],
    scan_type: str = "quick",
) -> dict:
    """
    Celery task to run compliance analysis on documents.
    
    Args:
        job_id: The job UUID string.
        document_ids: List of document UUID strings.
        scan_type: "quick" for 8 controls, "full" for all 51.
        
    Returns:
        Analysis results dictionary.
    """
    try:
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                _run_analysis(job_id, document_ids, scan_type)
            )
        finally:
            loop.close()
    except Exception as e:
        # Retry on failure
        raise self.retry(exc=e, countdown=60)
