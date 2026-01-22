"""
Remediation Tracker Service for ShieldAgent.

Tracks remediation tasks, assigns priorities, and monitors progress.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import uuid


class RemediationStatus(str, Enum):
    """Remediation task status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    VERIFIED = "verified"


class RemediationPriority(str, Enum):
    """Task priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class RemediationTask:
    """Individual remediation task."""
    id: str
    control_id: str
    control_title: str
    gap_description: str
    priority: RemediationPriority
    status: RemediationStatus
    category: str
    estimated_hours: int
    assigned_to: Optional[str]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    notes: List[str] = field(default_factory=list)
    evidence_links: List[str] = field(default_factory=list)
    action_items: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "control_id": self.control_id,
            "control_title": self.control_title,
            "gap_description": self.gap_description,
            "priority": self.priority.value,
            "status": self.status.value,
            "category": self.category,
            "estimated_hours": self.estimated_hours,
            "assigned_to": self.assigned_to,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "notes": self.notes,
            "evidence_links": self.evidence_links,
            "action_items": self.action_items,
        }


@dataclass
class RemediationPlan:
    """Complete remediation plan for an analysis."""
    id: str
    job_id: str
    organization_name: str
    created_at: datetime
    updated_at: datetime
    tasks: List[RemediationTask]
    target_completion_date: Optional[datetime]

    @property
    def total_tasks(self) -> int:
        return len(self.tasks)

    @property
    def completed_tasks(self) -> int:
        return sum(
            1 for t in self.tasks
            if t.status in [RemediationStatus.COMPLETED, RemediationStatus.VERIFIED]
        )

    @property
    def progress_percentage(self) -> float:
        if self.total_tasks == 0:
            return 100.0
        return (self.completed_tasks / self.total_tasks) * 100

    @property
    def total_estimated_hours(self) -> int:
        return sum(t.estimated_hours for t in self.tasks)

    @property
    def remaining_hours(self) -> int:
        return sum(
            t.estimated_hours for t in self.tasks
            if t.status not in [RemediationStatus.COMPLETED, RemediationStatus.VERIFIED]
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "job_id": self.job_id,
            "organization_name": self.organization_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tasks": [t.to_dict() for t in self.tasks],
            "target_completion_date": (
                self.target_completion_date.isoformat()
                if self.target_completion_date else None
            ),
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "progress_percentage": round(self.progress_percentage, 1),
            "total_estimated_hours": self.total_estimated_hours,
            "remaining_hours": self.remaining_hours,
        }


# Recommended action items by gap type
ACTION_ITEM_TEMPLATES = {
    "policy": [
        {"action": "Draft policy document", "hours": 4},
        {"action": "Review with stakeholders", "hours": 2},
        {"action": "Obtain management approval", "hours": 1},
        {"action": "Publish and communicate", "hours": 1},
    ],
    "procedure": [
        {"action": "Document current process", "hours": 4},
        {"action": "Identify gaps in process", "hours": 2},
        {"action": "Design improved procedure", "hours": 4},
        {"action": "Implement procedure", "hours": 4},
        {"action": "Train team members", "hours": 2},
    ],
    "technical": [
        {"action": "Evaluate technical solutions", "hours": 8},
        {"action": "Design implementation plan", "hours": 4},
        {"action": "Configure/deploy solution", "hours": 16},
        {"action": "Test in staging environment", "hours": 8},
        {"action": "Deploy to production", "hours": 4},
    ],
    "access": [
        {"action": "Audit current access rights", "hours": 4},
        {"action": "Define access requirements", "hours": 2},
        {"action": "Implement access changes", "hours": 4},
        {"action": "Document access policies", "hours": 2},
        {"action": "Set up periodic reviews", "hours": 2},
    ],
    "monitoring": [
        {"action": "Define monitoring requirements", "hours": 4},
        {"action": "Select monitoring tools", "hours": 4},
        {"action": "Configure alerts and dashboards", "hours": 8},
        {"action": "Document escalation procedures", "hours": 2},
        {"action": "Test monitoring coverage", "hours": 4},
    ],
}


class RemediationTracker:
    """
    Tracks and manages remediation tasks for compliance gaps.
    
    Features:
    - Auto-generates remediation tasks from analysis gaps
    - Prioritizes tasks based on severity and category
    - Estimates effort and due dates
    - Tracks progress and generates status reports
    """
    
    def __init__(self):
        self._plans: Dict[str, RemediationPlan] = {}
    
    def create_plan_from_analysis(
        self,
        job_id: str,
        analysis_results: Dict[str, Any],
        organization_name: str = "Organization",
        weeks_to_complete: int = 12,
    ) -> RemediationPlan:
        """
        Create a remediation plan from analysis results.
        
        Args:
            job_id: Analysis job ID
            analysis_results: Results from Gemini analysis
            organization_name: Organization name
            weeks_to_complete: Target weeks to complete all tasks
            
        Returns:
            RemediationPlan with auto-generated tasks
        """
        tasks = []
        now = datetime.now()
        
        controls = analysis_results.get("controls", [])
        
        for control in controls:
            if control.get("status") in ["fail", "needs_review"]:
                task = self._create_task_from_control(control, now)
                tasks.append(task)
        
        # Sort by priority
        priority_order = {
            RemediationPriority.CRITICAL: 0,
            RemediationPriority.HIGH: 1,
            RemediationPriority.MEDIUM: 2,
            RemediationPriority.LOW: 3,
        }
        tasks.sort(key=lambda t: priority_order[t.priority])
        
        # Assign due dates based on priority
        self._assign_due_dates(tasks, now, weeks_to_complete)
        
        plan = RemediationPlan(
            id=str(uuid.uuid4()),
            job_id=job_id,
            organization_name=organization_name,
            created_at=now,
            updated_at=now,
            tasks=tasks,
            target_completion_date=now + timedelta(weeks=weeks_to_complete),
        )
        
        self._plans[plan.id] = plan
        return plan
    
    def _create_task_from_control(
        self,
        control: Dict[str, Any],
        created_at: datetime,
    ) -> RemediationTask:
        """Create a remediation task from a failed/review control."""
        status = control.get("status", "fail")
        gaps = control.get("gaps", [])
        
        # Determine priority
        if status == "fail":
            priority = RemediationPriority.CRITICAL
        elif control.get("confidence", 0.5) < 0.5:
            priority = RemediationPriority.HIGH
        else:
            priority = RemediationPriority.MEDIUM
        
        # Determine gap type and action items
        gap_description = " ".join(gaps) if gaps else control.get("summary", "")
        gap_type = self._classify_gap_type(gap_description)
        action_items = self._get_action_items(gap_type)
        estimated_hours = sum(item["hours"] for item in action_items)
        
        return RemediationTask(
            id=str(uuid.uuid4()),
            control_id=control.get("control_id", ""),
            control_title=control.get("title", ""),
            gap_description=gap_description,
            priority=priority,
            status=RemediationStatus.NOT_STARTED,
            category=control.get("category", ""),
            estimated_hours=estimated_hours,
            assigned_to=None,
            due_date=None,
            created_at=created_at,
            updated_at=created_at,
            notes=[],
            evidence_links=[],
            action_items=action_items,
        )
    
    def _classify_gap_type(self, description: str) -> str:
        """Classify gap type based on description."""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ["policy", "document", "written"]):
            return "policy"
        elif any(word in description_lower for word in ["access", "permission", "role"]):
            return "access"
        elif any(word in description_lower for word in ["monitor", "log", "alert"]):
            return "monitoring"
        elif any(word in description_lower for word in ["implement", "deploy", "configure"]):
            return "technical"
        else:
            return "procedure"
    
    def _get_action_items(self, gap_type: str) -> List[Dict[str, Any]]:
        """Get action items template for gap type."""
        template = ACTION_ITEM_TEMPLATES.get(gap_type, ACTION_ITEM_TEMPLATES["procedure"])
        return [
            {
                "id": str(uuid.uuid4()),
                "action": item["action"],
                "hours": item["hours"],
                "completed": False,
            }
            for item in template
        ]
    
    def _assign_due_dates(
        self,
        tasks: List[RemediationTask],
        start_date: datetime,
        total_weeks: int,
    ) -> None:
        """Assign due dates based on priority."""
        critical_deadline = start_date + timedelta(weeks=2)
        high_deadline = start_date + timedelta(weeks=4)
        medium_deadline = start_date + timedelta(weeks=8)
        low_deadline = start_date + timedelta(weeks=total_weeks)
        
        for task in tasks:
            if task.priority == RemediationPriority.CRITICAL:
                task.due_date = critical_deadline
            elif task.priority == RemediationPriority.HIGH:
                task.due_date = high_deadline
            elif task.priority == RemediationPriority.MEDIUM:
                task.due_date = medium_deadline
            else:
                task.due_date = low_deadline
    
    def get_plan(self, plan_id: str) -> Optional[RemediationPlan]:
        """Get a remediation plan by ID."""
        return self._plans.get(plan_id)
    
    def update_task_status(
        self,
        plan_id: str,
        task_id: str,
        status: RemediationStatus,
        note: Optional[str] = None,
    ) -> Optional[RemediationTask]:
        """Update a task's status."""
        plan = self._plans.get(plan_id)
        if not plan:
            return None
        
        for task in plan.tasks:
            if task.id == task_id:
                task.status = status
                task.updated_at = datetime.now()
                if note:
                    task.notes.append(f"[{datetime.now().isoformat()}] {note}")
                plan.updated_at = datetime.now()
                return task
        
        return None
    
    def get_status_summary(self, plan_id: str) -> Dict[str, Any]:
        """Get a summary of remediation status."""
        plan = self._plans.get(plan_id)
        if not plan:
            return {}
        
        status_counts = {
            "not_started": 0,
            "in_progress": 0,
            "blocked": 0,
            "completed": 0,
            "verified": 0,
        }
        
        priority_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }
        
        overdue_tasks = []
        now = datetime.now()
        
        for task in plan.tasks:
            status_counts[task.status.value] += 1
            priority_counts[task.priority.value] += 1
            
            if (
                task.due_date
                and task.due_date < now
                and task.status not in [
                    RemediationStatus.COMPLETED,
                    RemediationStatus.VERIFIED,
                ]
            ):
                overdue_tasks.append(task.to_dict())
        
        return {
            "plan_id": plan_id,
            "progress_percentage": round(plan.progress_percentage, 1),
            "total_tasks": plan.total_tasks,
            "completed_tasks": plan.completed_tasks,
            "status_breakdown": status_counts,
            "priority_breakdown": priority_counts,
            "total_hours": plan.total_estimated_hours,
            "remaining_hours": plan.remaining_hours,
            "overdue_tasks": overdue_tasks,
            "days_until_target": (
                (plan.target_completion_date - now).days
                if plan.target_completion_date else None
            ),
        }


# Singleton instance
_tracker: RemediationTracker | None = None


def get_remediation_tracker() -> RemediationTracker:
    """Get or create remediation tracker instance."""
    global _tracker
    if _tracker is None:
        _tracker = RemediationTracker()
    return _tracker
