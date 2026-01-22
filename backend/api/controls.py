"""
Controls API endpoints for listing compliance controls.
Enhanced with full SOC 2 Trust Service Criteria.
"""

from fastapi import APIRouter, Query
from typing import Optional
import uuid

from services.soc2_controls import (
    get_all_controls,
    get_quick_scan_controls,
    get_control_by_id,
    get_control_categories,
    CONTROL_SUMMARY,
)
from schemas.control import ControlResponse, ControlListResponse

router = APIRouter()


@router.get("", response_model=ControlListResponse)
async def list_controls(
    framework: str = Query("soc2", description="Compliance framework"),
    category: Optional[str] = Query(None, description="Filter by category"),
    scan_type: str = Query("quick", description="'quick' for 8 key controls, 'full' for all"),
) -> ControlListResponse:
    """
    List all compliance controls for a framework.
    
    Args:
        framework: The compliance framework (default: soc2).
        category: Optional category filter.
        scan_type: 'quick' for key controls, 'full' for all 50+ controls.
    
    Returns:
        List of controls with total count.
    """
    # Get controls based on scan type
    if scan_type == "full":
        all_controls = get_all_controls()
    else:
        all_controls = get_quick_scan_controls()
    
    # Filter by category if provided
    if category:
        all_controls = [
            c for c in all_controls
            if category.lower() in c["category"].lower()
        ]
    
    # Convert to response format
    controls = []
    for control in all_controls:
        controls.append(
            ControlResponse(
                id=uuid.uuid5(uuid.NAMESPACE_DNS, control["control_id"]),
                control_id=control["control_id"],
                framework="SOC2",
                title=control["title"],
                description=control["description"],
                check_type="ai_prompt",
                category=control["category"],
                required_file_types="pdf,csv,json,txt",
            )
        )
    
    return ControlListResponse(
        controls=controls,
        total=len(controls),
    )


@router.get("/categories")
async def list_categories():
    """
    Get all SOC 2 control categories with counts.
    
    Returns:
        List of categories with control counts.
    """
    categories = get_control_categories()
    return {
        "categories": categories,
        "total_categories": len(categories),
    }


@router.get("/summary")
async def get_controls_summary():
    """
    Get summary statistics for all SOC 2 controls.
    
    Returns:
        Control statistics by category.
    """
    return {
        "summary": CONTROL_SUMMARY,
        "quick_scan_count": len(get_quick_scan_controls()),
        "full_scan_count": len(get_all_controls()),
    }


@router.get("/{control_id}")
async def get_control(control_id: str):
    """
    Get details for a specific control.
    
    Args:
        control_id: The control ID (e.g., CC6.1).
    
    Returns:
        Control details or 404 if not found.
    """
    control = get_control_by_id(control_id.upper())
    if not control:
        return {"error": f"Control {control_id} not found"}
    
    return {
        "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, control["control_id"])),
        "control_id": control["control_id"],
        "framework": "SOC2",
        "category": control["category"],
        "title": control["title"],
        "description": control["description"],
        "check_prompt": control["check_prompt"],
    }
