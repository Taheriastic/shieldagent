"""
Celery application configuration for ShieldAgent background tasks.
"""

from celery import Celery

from core.config import settings


# Create Celery app
celery_app = Celery(
    "shieldagent",
    broker=settings.celery_broker,
    backend=settings.celery_backend,
    include=["worker.tasks"],
)

# Configure Celery
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task tracking
    task_track_started=True,
    task_time_limit=600,  # 10 minutes max per task
    task_soft_time_limit=540,  # 9 minutes soft limit
    
    # Result expiration
    result_expires=86400,  # 24 hours
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_concurrency=2,
    
    # Retry settings
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
