"""
Gemini AI Service for SOC 2 compliance document analysis.
Uses Google's Gemini API to analyze documents against compliance controls.
"""

import json
import re
from typing import Any
from pathlib import Path

import google.generativeai as genai

from core.config import settings
from services.soc2_controls import (
    get_all_controls,
    get_quick_scan_controls,
    get_control_by_id,
    get_control_categories,
    CONTROL_SUMMARY,
)


# Legacy controls for backwards compatibility
SOC2_CONTROLS = [
    {
        "control_id": "CC6.1",
        "category": "Logical and Physical Access Controls",
        "title": "Logical Access Security",
        "description": "The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events.",
        "check_prompt": """Analyze the provided documents for evidence of logical access security controls.
Look for:
- Authentication mechanisms (passwords, MFA, SSO)
- Access control lists or role-based access control (RBAC)
- User provisioning and deprovisioning procedures
- Access review processes
- Privileged access management

Provide your analysis as JSON with these fields:
- status: "pass", "fail", or "needs_review"
- confidence: 0.0 to 1.0
- summary: Brief explanation of findings
- evidence_quote: Direct quote from document supporting the finding
- gaps: List of any gaps or missing elements""",
    },
    {
        "control_id": "CC6.2",
        "category": "Logical and Physical Access Controls",
        "title": "User Registration and Authorization",
        "description": "Prior to issuing system credentials and granting system access, the entity registers and authorizes new internal and external users.",
        "check_prompt": """Analyze the provided documents for evidence of user registration and authorization procedures.
Look for:
- New user onboarding procedures
- Authorization approval workflows
- Background check requirements
- System access request forms
- Manager approval requirements

Provide your analysis as JSON with these fields:
- status: "pass", "fail", or "needs_review"
- confidence: 0.0 to 1.0
- summary: Brief explanation of findings
- evidence_quote: Direct quote from document supporting the finding
- gaps: List of any gaps or missing elements""",
    },
    {
        "control_id": "CC6.3",
        "category": "Logical and Physical Access Controls",
        "title": "User Access Removal",
        "description": "The entity removes access to protected information assets when the access is no longer required.",
        "check_prompt": """Analyze the provided documents for evidence of user access removal procedures.
Look for:
- Termination procedures for access removal
- Transfer/role change access review
- Timely revocation of access
- Periodic access reviews
- Automated deprovisioning

Provide your analysis as JSON with these fields:
- status: "pass", "fail", or "needs_review"
- confidence: 0.0 to 1.0
- summary: Brief explanation of findings
- evidence_quote: Direct quote from document supporting the finding
- gaps: List of any gaps or missing elements""",
    },
    {
        "control_id": "CC7.2",
        "category": "System Operations",
        "title": "Security Incident Monitoring",
        "description": "The entity monitors system components and the operation of those components for anomalies that are indicative of malicious acts, natural disasters, and errors affecting the entity's ability to meet its objectives.",
        "check_prompt": """Analyze the provided documents for evidence of security incident monitoring.
Look for:
- Security monitoring tools (SIEM, IDS/IPS)
- Log collection and analysis
- Alerting thresholds and procedures
- 24/7 monitoring capabilities
- Incident detection procedures

Provide your analysis as JSON with these fields:
- status: "pass", "fail", or "needs_review"
- confidence: 0.0 to 1.0
- summary: Brief explanation of findings
- evidence_quote: Direct quote from document supporting the finding
- gaps: List of any gaps or missing elements""",
    },
    {
        "control_id": "CC7.3",
        "category": "System Operations",
        "title": "Security Incident Response",
        "description": "The entity evaluates security events to determine whether they could or have resulted in a failure of the entity to meet its objectives and, if so, takes actions to prevent or address such failures.",
        "check_prompt": """Analyze the provided documents for evidence of security incident response procedures.
Look for:
- Incident response plan/playbooks
- Incident classification and severity levels
- Response team roles and responsibilities
- Communication procedures
- Post-incident review process

Provide your analysis as JSON with these fields:
- status: "pass", "fail", or "needs_review"
- confidence: 0.0 to 1.0
- summary: Brief explanation of findings
- evidence_quote: Direct quote from document supporting the finding
- gaps: List of any gaps or missing elements""",
    },
    {
        "control_id": "CC8.1",
        "category": "Change Management",
        "title": "Change Management Process",
        "description": "The entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures to meet its objectives.",
        "check_prompt": """Analyze the provided documents for evidence of change management processes.
Look for:
- Change request procedures
- Change approval workflows
- Testing requirements before deployment
- Documentation requirements
- Rollback procedures

Provide your analysis as JSON with these fields:
- status: "pass", "fail", or "needs_review"
- confidence: 0.0 to 1.0
- summary: Brief explanation of findings
- evidence_quote: Direct quote from document supporting the finding
- gaps: List of any gaps or missing elements""",
    },
    {
        "control_id": "CC9.1",
        "category": "Risk Mitigation",
        "title": "Risk Assessment Process",
        "description": "The entity identifies, selects, and develops risk mitigation activities for risks arising from potential business disruptions.",
        "check_prompt": """Analyze the provided documents for evidence of risk assessment processes.
Look for:
- Risk assessment methodology
- Risk identification procedures
- Risk rating/scoring criteria
- Risk treatment plans
- Regular risk review schedule

Provide your analysis as JSON with these fields:
- status: "pass", "fail", or "needs_review"
- confidence: 0.0 to 1.0
- summary: Brief explanation of findings
- evidence_quote: Direct quote from document supporting the finding
- gaps: List of any gaps or missing elements""",
    },
    {
        "control_id": "A1.2",
        "category": "Availability",
        "title": "Backup and Recovery",
        "description": "The entity authorizes, designs, develops or acquires, implements, operates, approves, maintains, and monitors environmental protections, software, data backup processes, and recovery infrastructure to meet its objectives.",
        "check_prompt": """Analyze the provided documents for evidence of backup and recovery procedures.
Look for:
- Backup policies and schedules
- Backup testing/verification
- Recovery time objectives (RTO)
- Recovery point objectives (RPO)
- Disaster recovery procedures

Provide your analysis as JSON with these fields:
- status: "pass", "fail", or "needs_review"
- confidence: 0.0 to 1.0
- summary: Brief explanation of findings
- evidence_quote: Direct quote from document supporting the finding
- gaps: List of any gaps or missing elements""",
    },
]


class GeminiService:
    """Service for interacting with Google Gemini AI for compliance analysis."""

    def __init__(self, scan_type: str = "quick"):
        """
        Initialize Gemini client with API key from settings.
        
        Args:
            scan_type: "quick" for 8 key controls, "full" for all 50+ controls
        """
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        self.scan_type = scan_type
        
        # Use comprehensive controls or quick scan
        if scan_type == "full":
            self.controls = get_all_controls()
        else:
            self.controls = get_quick_scan_controls()

    def get_controls(self) -> list[dict]:
        """Get all SOC 2 controls for analysis."""
        return self.controls
    
    def get_all_available_controls(self) -> list[dict]:
        """Get all available SOC 2 controls (full list)."""
        return get_all_controls()
    
    def get_control_categories_summary(self) -> list[dict]:
        """Get summary of control categories."""
        return get_control_categories()
    
    def get_control_stats(self) -> dict:
        """Get control statistics."""
        return CONTROL_SUMMARY

    async def extract_document_text(self, file_path: str) -> str:
        """
        Extract text content from a document file.
        
        Args:
            file_path: Path to the document file.
            
        Returns:
            Extracted text content.
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        file_ext = path.suffix.lower()
        
        if file_ext == ".pdf":
            return await self._extract_pdf_text(path)
        elif file_ext == ".csv":
            return await self._extract_csv_text(path)
        elif file_ext == ".json":
            return await self._extract_json_text(path)
        elif file_ext in (".txt", ".md"):
            return path.read_text(encoding="utf-8")
        else:
            # Try to read as plain text
            try:
                return path.read_text(encoding="utf-8")
            except Exception:
                raise ValueError(f"Unsupported file type: {file_ext}")

    async def _extract_pdf_text(self, path: Path) -> str:
        """Extract text from PDF file using PyMuPDF."""
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(str(path))
            text_parts = []
            
            for page_num, page in enumerate(doc, 1):
                text = page.get_text()
                if text.strip():
                    text_parts.append(f"--- Page {page_num} ---\n{text}")
            
            doc.close()
            return "\n\n".join(text_parts)
        except ImportError:
            raise ImportError("PyMuPDF (fitz) required for PDF processing. Install with: pip install PyMuPDF")

    async def _extract_csv_text(self, path: Path) -> str:
        """Extract text from CSV file."""
        import csv
        
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Format as readable table
        if not rows:
            return ""
        
        # Get headers
        headers = rows[0]
        text_parts = [f"CSV Document with columns: {', '.join(headers)}\n"]
        
        for i, row in enumerate(rows[1:], 1):
            row_text = " | ".join(f"{h}: {v}" for h, v in zip(headers, row) if v)
            text_parts.append(f"Row {i}: {row_text}")
        
        return "\n".join(text_parts)

    async def _extract_json_text(self, path: Path) -> str:
        """Extract text from JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Convert to formatted string
        return f"JSON Document:\n{json.dumps(data, indent=2)}"

    async def analyze_control(
        self,
        control: dict,
        document_texts: list[str],
    ) -> dict[str, Any]:
        """
        Analyze documents against a specific SOC 2 control.
        
        Args:
            control: The control definition with check_prompt.
            document_texts: List of document text contents.
            
        Returns:
            Analysis result with status, confidence, summary, etc.
        """
        # Prepare document content
        combined_text = "\n\n=== DOCUMENT ===\n\n".join(document_texts)
        
        # Truncate if too long (Gemini has context limits)
        max_chars = 30000
        if len(combined_text) > max_chars:
            combined_text = combined_text[:max_chars] + "\n\n[Document truncated due to length...]"
        
        # Build the prompt
        prompt = f"""You are a SOC 2 compliance expert analyzing documents for evidence of security controls.

CONTROL BEING EVALUATED:
- Control ID: {control['control_id']}
- Category: {control['category']}
- Title: {control['title']}
- Description: {control['description']}

ANALYSIS INSTRUCTIONS:
{control['check_prompt']}

DOCUMENTS TO ANALYZE:
{combined_text}

IMPORTANT: Respond ONLY with valid JSON in this exact format:
{{
    "status": "pass" | "fail" | "needs_review",
    "confidence": 0.0 to 1.0,
    "summary": "Brief explanation of your findings",
    "evidence_quote": "Direct quote from document if found, or null",
    "gaps": ["List of identified gaps or missing elements"]
}}"""

        try:
            # Call Gemini API
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            result = self._parse_json_response(response_text)
            result["raw_response"] = response_text
            result["control_id"] = control["control_id"]
            
            return result
            
        except Exception as e:
            return {
                "control_id": control["control_id"],
                "status": "error",
                "confidence": 0.0,
                "summary": f"Error during analysis: {str(e)}",
                "evidence_quote": None,
                "gaps": ["Analysis could not be completed"],
                "raw_response": str(e),
            }

    def _parse_json_response(self, response_text: str) -> dict[str, Any]:
        """Parse JSON from Gemini response, handling markdown code blocks."""
        # Try to extract JSON from markdown code block
        json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
        
        # Try direct JSON parse
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to find JSON object in text
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
        
        # Return default structure if parsing fails
        return {
            "status": "needs_review",
            "confidence": 0.0,
            "summary": "Could not parse AI response",
            "evidence_quote": None,
            "gaps": ["Response parsing failed"],
        }

    async def analyze_documents(
        self,
        document_paths: list[str],
        progress_callback: callable = None,
    ) -> dict[str, Any]:
        """
        Analyze multiple documents against all SOC 2 controls.
        
        Args:
            document_paths: List of document file paths.
            progress_callback: Optional callback for progress updates.
            
        Returns:
            Complete analysis results with evidence and gaps.
        """
        # Extract text from all documents
        document_texts = []
        for path in document_paths:
            try:
                text = await self.extract_document_text(path)
                document_texts.append(text)
            except Exception as e:
                document_texts.append(f"[Error extracting {path}: {str(e)}]")
        
        # Analyze each control
        results = {
            "evidence_items": [],
            "gaps": [],
            "summary": {
                "total_controls": len(self.controls),
                "passing": 0,
                "failing": 0,
                "needs_review": 0,
            }
        }
        
        for i, control in enumerate(self.controls):
            if progress_callback:
                progress_callback(i, len(self.controls), control["control_id"])
            
            analysis = await self.analyze_control(control, document_texts)
            
            # Build evidence item
            evidence = {
                "control_id": control["control_id"],
                "status": analysis.get("status", "needs_review"),
                "confidence": analysis.get("confidence", 0.0),
                "summary": analysis.get("summary", ""),
                "evidence_quote": analysis.get("evidence_quote"),
                "raw_llm_response": analysis.get("raw_response"),
            }
            results["evidence_items"].append(evidence)
            
            # Update summary counts
            status = analysis.get("status", "needs_review")
            if status == "pass":
                results["summary"]["passing"] += 1
            elif status == "fail":
                results["summary"]["failing"] += 1
            else:
                results["summary"]["needs_review"] += 1
            
            # Add gaps
            gaps = analysis.get("gaps", [])
            for gap_desc in gaps:
                if gap_desc and gap_desc not in ["None", "N/A", ""]:
                    severity = "high" if status == "fail" else "medium"
                    results["gaps"].append({
                        "control_id": control["control_id"],
                        "severity": severity,
                        "description": gap_desc,
                        "remediation_suggestion": self._get_remediation(control["control_id"], gap_desc),
                    })
        
        return results

    def _get_remediation(self, control_id: str, gap_description: str) -> str:
        """Generate remediation suggestion for a gap."""
        remediations = {
            "CC6.1": "Implement multi-factor authentication, establish role-based access controls, and document access policies.",
            "CC6.2": "Create formal user registration procedures with management approval workflow and maintain access request records.",
            "CC6.3": "Implement automated deprovisioning, conduct quarterly access reviews, and document termination procedures.",
            "CC7.2": "Deploy SIEM solution, configure alerting thresholds, and establish 24/7 monitoring procedures.",
            "CC7.3": "Develop incident response playbooks, define severity levels, and conduct regular tabletop exercises.",
            "CC8.1": "Implement change management ticketing system, require testing before deployment, and maintain change logs.",
            "CC9.1": "Conduct annual risk assessments, maintain risk register, and document risk treatment decisions.",
            "A1.2": "Define RTO/RPO objectives, implement automated backups, and conduct regular recovery testing.",
        }
        return remediations.get(control_id, "Review control requirements and implement appropriate measures.")


# Singleton instance
_gemini_service: GeminiService | None = None


def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
