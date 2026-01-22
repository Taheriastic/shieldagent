"""
Reports API endpoints for generating compliance reports.
"""

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from datetime import datetime

from services.pdf_report import get_pdf_generator

router = APIRouter()


@router.get("/pdf/{job_id}")
async def generate_pdf_report(
    job_id: str,
    organization_name: str = Query(
        "Your Organization",
        description="Organization name for report",
    ),
):
    """
    Generate a PDF compliance report for a completed analysis job.
    
    Args:
        job_id: The analysis job ID
        organization_name: Name to appear on the report
        
    Returns:
        PDF file as streaming response
    """
    # For demo, generate a sample report
    # In production, you'd fetch actual job results from database
    
    pdf_generator = get_pdf_generator()
    
    # Sample results for demonstration
    sample_results = {
        "total_controls": 8,
        "passing": 5,
        "failing": 1,
        "needs_review": 2,
        "controls": [
            {
                "control_id": "CC6.1",
                "category": "Logical and Physical Access",
                "title": "Logical Access Security",
                "status": "pass",
                "confidence": 0.92,
                "summary": "Strong access controls found including MFA, RBAC, and quarterly access reviews.",
                "evidence_quote": "Multi-factor authentication required for all remote access",
                "gaps": [],
            },
            {
                "control_id": "CC6.2",
                "category": "Logical and Physical Access",
                "title": "User Registration",
                "status": "pass",
                "confidence": 0.88,
                "summary": "Documented user onboarding procedures with manager approval workflow.",
                "evidence_quote": "HR notifies IT of new hires 3 days before start date",
                "gaps": [],
            },
            {
                "control_id": "CC6.3",
                "category": "Logical and Physical Access",
                "title": "Access Removal",
                "status": "needs_review",
                "confidence": 0.65,
                "summary": "Some termination procedures exist but automated deprovisioning not documented.",
                "gaps": ["No automated deprovisioning process", "Missing transfer access review procedures"],
            },
            {
                "control_id": "CC7.2",
                "category": "System Operations",
                "title": "Security Monitoring",
                "status": "needs_review",
                "confidence": 0.55,
                "summary": "Basic monitoring mentioned but lacks details on SIEM and 24/7 coverage.",
                "gaps": ["No SIEM solution documented", "Missing 24/7 monitoring procedures"],
            },
            {
                "control_id": "CC7.3",
                "category": "System Operations",
                "title": "Incident Response",
                "status": "pass",
                "confidence": 0.85,
                "summary": "Incident response plan with severity levels and communication procedures in place.",
                "evidence_quote": "Security incidents reported within 1 hour to security team",
                "gaps": [],
            },
            {
                "control_id": "CC8.1",
                "category": "Change Management",
                "title": "Change Management Process",
                "status": "pass",
                "confidence": 0.90,
                "summary": "Formal change approval process with CAB review and documentation requirements.",
                "evidence_quote": "All changes require CAB approval before production deployment",
                "gaps": [],
            },
            {
                "control_id": "CC9.1",
                "category": "Risk Mitigation",
                "title": "Risk Assessment",
                "status": "fail",
                "confidence": 0.78,
                "summary": "No documented risk assessment methodology or risk register was found.",
                "gaps": [
                    "Missing formal risk assessment methodology",
                    "No risk register maintained",
                    "No documented risk treatment plans"
                ],
            },
            {
                "control_id": "A1.2",
                "category": "Availability",
                "title": "Backup and Recovery",
                "status": "pass",
                "confidence": 0.95,
                "summary": "Comprehensive backup procedures with defined RTO/RPO and regular testing.",
                "evidence_quote": "Daily incremental backups, weekly full backups, 4-hour RTO, 1-hour RPO",
                "gaps": [],
            },
        ],
    }
    
    # Generate PDF
    pdf_buffer = pdf_generator.generate_report(
        organization_name=organization_name,
        analysis_results=sample_results,
        report_date=datetime.now(),
    )
    
    # Generate filename
    filename = f"SOC2_Compliance_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/demo")
async def generate_demo_report(
    organization_name: str = Query("Demo Organization", description="Organization name"),
):
    """
    Generate a demo PDF report without authentication.
    Perfect for showcasing the application.
    """
    pdf_generator = get_pdf_generator()
    
    demo_results = {
        "total_controls": 8,
        "passing": 5,
        "failing": 1,
        "needs_review": 2,
        "controls": [
            {
                "control_id": "CC6.1",
                "category": "Logical and Physical Access",
                "title": "Logical Access Security",
                "status": "pass",
                "confidence": 0.92,
                "summary": "Strong access controls including MFA, RBAC, and quarterly access reviews are implemented.",
                "evidence_quote": "Multi-factor authentication required for all remote access and admin accounts",
                "gaps": [],
            },
            {
                "control_id": "CC6.2",
                "category": "Logical and Physical Access",
                "title": "User Registration",
                "status": "pass",
                "confidence": 0.88,
                "summary": "Documented user onboarding with HR notification, manager approval, and background checks.",
                "evidence_quote": "HR notifies IT of new hires 3 days before start date, manager approval required",
                "gaps": [],
            },
            {
                "control_id": "CC6.3",
                "category": "Logical and Physical Access",
                "title": "Access Removal",
                "status": "needs_review",
                "confidence": 0.65,
                "summary": "Termination procedures exist but automated deprovisioning needs documentation.",
                "gaps": ["Automated deprovisioning not documented", "Role transfer procedures missing"],
            },
            {
                "control_id": "CC7.2",
                "category": "System Operations",
                "title": "Security Monitoring",
                "status": "needs_review",
                "confidence": 0.55,
                "summary": "Basic monitoring in place but SIEM solution and 24/7 coverage need verification.",
                "gaps": ["SIEM implementation details needed", "24/7 SOC coverage not confirmed"],
            },
            {
                "control_id": "CC7.3",
                "category": "System Operations",
                "title": "Incident Response",
                "status": "pass",
                "confidence": 0.85,
                "summary": "Comprehensive incident response plan with severity classification and escalation paths.",
                "evidence_quote": "Security incidents reported within 1 hour, post-mortem within 5 days",
                "gaps": [],
            },
            {
                "control_id": "CC8.1",
                "category": "Change Management",
                "title": "Change Management Process",
                "status": "pass",
                "confidence": 0.90,
                "summary": "Formal CAB approval process with testing requirements and rollback procedures.",
                "evidence_quote": "All production changes require CAB approval and documented rollback plan",
                "gaps": [],
            },
            {
                "control_id": "CC9.1",
                "category": "Risk Mitigation",
                "title": "Risk Assessment",
                "status": "fail",
                "confidence": 0.78,
                "summary": "Critical gap: No documented risk assessment methodology or risk register found.",
                "gaps": [
                    "No formal risk assessment methodology",
                    "Risk register not maintained",
                    "Risk treatment plans not documented",
                    "Annual risk review not evidenced"
                ],
            },
            {
                "control_id": "A1.2",
                "category": "Availability",
                "title": "Backup and Recovery",
                "status": "pass",
                "confidence": 0.95,
                "summary": "Excellent backup strategy with defined RTO/RPO, automated backups, and DR testing.",
                "evidence_quote": "Daily incremental, weekly full backups; 4-hour RTO, 1-hour RPO; annual DR tests",
                "gaps": [],
            },
        ],
    }
    
    pdf_buffer = pdf_generator.generate_report(
        organization_name=organization_name,
        analysis_results=demo_results,
        report_date=datetime.now(),
    )
    
    filename = f"ShieldAgent_Demo_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
