"""
Risk Analysis API endpoints.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

from services.risk_calculator import get_risk_calculator, RiskScore
from services.remediation_tracker import (
    get_remediation_tracker,
    RemediationStatus,
)

router = APIRouter()


class RiskAnalysisResponse(BaseModel):
    """Risk analysis response."""
    overall_score: float
    risk_level: str
    category_scores: Dict[str, float]
    compliance_percentage: float
    gap_count: int
    critical_gaps: List[Dict[str, Any]]
    recommendations: List[str]
    estimated_remediation_hours: int
    audit_readiness: str


class RemediationPlanResponse(BaseModel):
    """Remediation plan response."""
    id: str
    job_id: str
    organization_name: str
    total_tasks: int
    completed_tasks: int
    progress_percentage: float
    total_estimated_hours: int
    remaining_hours: int
    tasks: List[Dict[str, Any]]


class UpdateTaskRequest(BaseModel):
    """Request to update task status."""
    status: str
    note: Optional[str] = None


@router.post("/calculate", response_model=RiskAnalysisResponse)
async def calculate_risk_score(
    analysis_results: Dict[str, Any],
):
    """
    Calculate risk score from analysis results.
    
    Returns comprehensive risk analysis including:
    - Overall compliance score
    - Risk level assessment
    - Category breakdown
    - Gap identification
    - Remediation recommendations
    """
    calculator = get_risk_calculator()
    
    try:
        result = calculator.calculate_risk_score(analysis_results)
        
        return RiskAnalysisResponse(
            overall_score=result.overall_score,
            risk_level=result.risk_level.value,
            category_scores=result.category_scores,
            compliance_percentage=result.compliance_percentage,
            gap_count=result.gap_count,
            critical_gaps=result.critical_gaps,
            recommendations=result.recommendations,
            estimated_remediation_hours=result.estimated_remediation_hours,
            audit_readiness=result.audit_readiness,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/demo")
async def get_demo_risk_analysis():
    """
    Get a demo risk analysis with sample data.
    """
    calculator = get_risk_calculator()
    
    # Sample data for demo
    sample_results = {
        "controls": [
            {
                "control_id": "CC6.1",
                "category": "Logical and Physical Access",
                "title": "Logical Access Security",
                "status": "pass",
                "confidence": 0.92,
                "summary": "Strong access controls implemented.",
                "gaps": [],
            },
            {
                "control_id": "CC6.2",
                "category": "Logical and Physical Access",
                "title": "User Registration",
                "status": "pass",
                "confidence": 0.88,
                "summary": "Good user management procedures.",
                "gaps": [],
            },
            {
                "control_id": "CC6.3",
                "category": "Logical and Physical Access",
                "title": "Access Removal",
                "status": "needs_review",
                "confidence": 0.65,
                "summary": "Some procedures exist but gaps found.",
                "gaps": [
                    "No automated deprovisioning",
                    "Missing transfer procedures",
                ],
            },
            {
                "control_id": "CC7.2",
                "category": "System Operations",
                "title": "Security Monitoring",
                "status": "needs_review",
                "confidence": 0.55,
                "summary": "Basic monitoring in place.",
                "gaps": ["SIEM not documented", "24/7 coverage unclear"],
            },
            {
                "control_id": "CC7.3",
                "category": "System Operations",
                "title": "Incident Response",
                "status": "pass",
                "confidence": 0.85,
                "summary": "Incident response plan exists.",
                "gaps": [],
            },
            {
                "control_id": "CC8.1",
                "category": "Change Management",
                "title": "Change Process",
                "status": "pass",
                "confidence": 0.90,
                "summary": "CAB process in place.",
                "gaps": [],
            },
            {
                "control_id": "CC9.1",
                "category": "Risk Assessment",
                "title": "Risk Assessment",
                "status": "fail",
                "confidence": 0.78,
                "summary": "No documented risk methodology.",
                "gaps": [
                    "No risk methodology",
                    "No risk register",
                    "No risk treatment plans",
                ],
            },
            {
                "control_id": "A1.2",
                "category": "Availability",
                "title": "Backup and Recovery",
                "status": "pass",
                "confidence": 0.95,
                "summary": "Excellent backup strategy.",
                "gaps": [],
            },
        ]
    }
    
    result = calculator.calculate_risk_score(sample_results)
    
    return {
        "overall_score": result.overall_score,
        "risk_level": result.risk_level.value,
        "category_scores": result.category_scores,
        "compliance_percentage": result.compliance_percentage,
        "gap_count": result.gap_count,
        "critical_gaps": result.critical_gaps,
        "recommendations": result.recommendations,
        "estimated_remediation_hours": result.estimated_remediation_hours,
        "audit_readiness": result.audit_readiness,
        "analysis_timestamp": datetime.now().isoformat(),
    }


@router.post("/remediation/plan")
async def create_remediation_plan(
    job_id: str = Query(..., description="Analysis job ID"),
    organization_name: str = Query("Organization", description="Org name"),
    weeks_to_complete: int = Query(12, description="Weeks to complete"),
    analysis_results: Dict[str, Any] = None,
):
    """
    Create a remediation plan from analysis results.
    
    Auto-generates prioritized tasks with:
    - Estimated hours
    - Due dates
    - Action item checklists
    """
    tracker = get_remediation_tracker()
    
    # Use sample data if none provided
    if not analysis_results or not analysis_results.get("controls"):
        analysis_results = {
            "controls": [
                {
                    "control_id": "CC6.3",
                    "category": "Access Control",
                    "title": "Access Removal",
                    "status": "needs_review",
                    "confidence": 0.65,
                    "summary": "Gaps in access removal procedures.",
                    "gaps": [
                        "No automated deprovisioning",
                        "Missing transfer procedures",
                    ],
                },
                {
                    "control_id": "CC7.2",
                    "category": "Monitoring",
                    "title": "Security Monitoring",
                    "status": "needs_review",
                    "confidence": 0.55,
                    "summary": "Monitoring gaps identified.",
                    "gaps": ["SIEM not implemented", "24/7 coverage needed"],
                },
                {
                    "control_id": "CC9.1",
                    "category": "Risk Management",
                    "title": "Risk Assessment",
                    "status": "fail",
                    "confidence": 0.78,
                    "summary": "Missing risk assessment program.",
                    "gaps": [
                        "No risk methodology",
                        "No risk register",
                        "No treatment plans",
                    ],
                },
            ]
        }
    
    plan = tracker.create_plan_from_analysis(
        job_id=job_id,
        analysis_results=analysis_results,
        organization_name=organization_name,
        weeks_to_complete=weeks_to_complete,
    )
    
    return plan.to_dict()


@router.get("/remediation/plan/{plan_id}")
async def get_remediation_plan(plan_id: str):
    """Get a remediation plan by ID."""
    tracker = get_remediation_tracker()
    plan = tracker.get_plan(plan_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return plan.to_dict()


@router.get("/remediation/plan/{plan_id}/summary")
async def get_remediation_summary(plan_id: str):
    """Get remediation progress summary."""
    tracker = get_remediation_tracker()
    summary = tracker.get_status_summary(plan_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return summary


@router.patch("/remediation/plan/{plan_id}/task/{task_id}")
async def update_task(
    plan_id: str,
    task_id: str,
    request: UpdateTaskRequest,
):
    """Update a remediation task status."""
    tracker = get_remediation_tracker()
    
    try:
        status = RemediationStatus(request.status)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status: {request.status}",
        )
    
    task = tracker.update_task_status(
        plan_id=plan_id,
        task_id=task_id,
        status=status,
        note=request.note,
    )
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task.to_dict()
