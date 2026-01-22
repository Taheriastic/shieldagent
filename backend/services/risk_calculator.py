"""
Risk Score Calculator Service for ShieldAgent.

Provides intelligent risk scoring based on control status, 
categories, and industry benchmarks.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class RiskLevel(str, Enum):
    """Risk severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


@dataclass
class RiskScore:
    """Risk score result."""
    overall_score: float  # 0-100, higher is better
    risk_level: RiskLevel
    category_scores: Dict[str, float]
    compliance_percentage: float
    gap_count: int
    critical_gaps: List[Dict[str, Any]]
    recommendations: List[str]
    estimated_remediation_hours: int
    audit_readiness: str  # "Ready", "Almost Ready", "Needs Work", "Not Ready"


# Control category weights based on auditor focus areas
CATEGORY_WEIGHTS = {
    "Security": 0.35,
    "Availability": 0.20,
    "Processing Integrity": 0.15,
    "Confidentiality": 0.15,
    "Privacy": 0.15,
}

# Subcategory importance within Security (CC controls)
CC_SUBCATEGORY_WEIGHTS = {
    "Control Environment": 0.10,
    "Communication and Information": 0.10,
    "Risk Assessment": 0.15,
    "Monitoring Activities": 0.10,
    "Control Activities": 0.10,
    "Logical and Physical Access": 0.20,
    "System Operations": 0.15,
    "Change Management": 0.10,
}

# Estimated remediation hours by control type
REMEDIATION_HOURS = {
    "policy": 8,
    "procedure": 16,
    "technical": 40,
    "training": 24,
    "monitoring": 32,
}


class RiskCalculator:
    """
    Calculates comprehensive risk scores for SOC 2 compliance.
    
    Uses weighted scoring based on:
    - Control category importance
    - Pass/fail/review status
    - AI confidence levels
    - Gap severity
    """
    
    def calculate_risk_score(
        self,
        analysis_results: Dict[str, Any],
    ) -> RiskScore:
        """
        Calculate comprehensive risk score from analysis results.
        
        Args:
            analysis_results: Results from Gemini analysis
            
        Returns:
            RiskScore with detailed breakdown
        """
        controls = analysis_results.get("controls", [])
        
        if not controls:
            return RiskScore(
                overall_score=0,
                risk_level=RiskLevel.CRITICAL,
                category_scores={},
                compliance_percentage=0,
                gap_count=0,
                critical_gaps=[],
                recommendations=["No controls analyzed yet"],
                estimated_remediation_hours=0,
                audit_readiness="Not Ready",
            )
        
        # Calculate category scores
        category_scores = self._calculate_category_scores(controls)
        
        # Calculate weighted overall score
        overall_score = self._calculate_weighted_score(category_scores)
        
        # Determine risk level
        risk_level = self._determine_risk_level(overall_score)
        
        # Calculate compliance percentage
        passing = sum(1 for c in controls if c.get("status") == "pass")
        compliance_percentage = (passing / len(controls)) * 100
        
        # Identify gaps
        gaps = self._identify_gaps(controls)
        critical_gaps = [g for g in gaps if g["severity"] == "critical"]
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            category_scores, gaps, compliance_percentage
        )
        
        # Estimate remediation time
        remediation_hours = self._estimate_remediation_time(gaps)
        
        # Determine audit readiness
        audit_readiness = self._determine_audit_readiness(
            overall_score, len(critical_gaps), compliance_percentage
        )
        
        return RiskScore(
            overall_score=round(overall_score, 1),
            risk_level=risk_level,
            category_scores=category_scores,
            compliance_percentage=round(compliance_percentage, 1),
            gap_count=len(gaps),
            critical_gaps=critical_gaps,
            recommendations=recommendations,
            estimated_remediation_hours=remediation_hours,
            audit_readiness=audit_readiness,
        )
    
    def _calculate_category_scores(
        self,
        controls: List[Dict[str, Any]],
    ) -> Dict[str, float]:
        """Calculate scores for each Trust Service Category."""
        category_results: Dict[str, List[float]] = {}
        
        for control in controls:
            category = control.get("category", "Security")
            # Map subcategories to main categories
            main_category = self._map_to_main_category(category)
            
            if main_category not in category_results:
                category_results[main_category] = []
            
            # Calculate control score (0-100)
            score = self._calculate_control_score(control)
            category_results[main_category].append(score)
        
        # Average scores per category
        category_scores = {}
        for category, scores in category_results.items():
            if scores:
                category_scores[category] = sum(scores) / len(scores)
            else:
                category_scores[category] = 0
        
        return category_scores
    
    def _calculate_control_score(self, control: Dict[str, Any]) -> float:
        """Calculate score for a single control."""
        status = control.get("status", "fail")
        confidence = control.get("confidence", 0.5)
        
        base_score = {
            "pass": 100,
            "needs_review": 50,
            "fail": 0,
        }.get(status, 0)
        
        # Adjust by confidence (higher confidence = more weight)
        adjusted_score = base_score * (0.5 + (confidence * 0.5))
        
        return min(100, max(0, adjusted_score))
    
    def _map_to_main_category(self, category: str) -> str:
        """Map subcategory names to main TSC categories."""
        security_subcategories = [
            "Control Environment",
            "Communication and Information",
            "Risk Assessment",
            "Monitoring Activities",
            "Control Activities",
            "Logical and Physical Access",
            "System Operations",
            "Change Management",
            "Risk Mitigation",
        ]
        
        if category in security_subcategories or category == "Security":
            return "Security"
        elif category == "Availability":
            return "Availability"
        elif "Processing" in category or "Integrity" in category:
            return "Processing Integrity"
        elif category == "Confidentiality":
            return "Confidentiality"
        elif category == "Privacy":
            return "Privacy"
        else:
            return "Security"  # Default to security
    
    def _calculate_weighted_score(
        self,
        category_scores: Dict[str, float],
    ) -> float:
        """Calculate weighted overall score."""
        total_weight = 0
        weighted_sum = 0
        
        for category, score in category_scores.items():
            weight = CATEGORY_WEIGHTS.get(category, 0.1)
            weighted_sum += score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0
        
        return weighted_sum / total_weight * 100 / 100
    
    def _determine_risk_level(self, score: float) -> RiskLevel:
        """Determine risk level from score."""
        if score >= 90:
            return RiskLevel.MINIMAL
        elif score >= 75:
            return RiskLevel.LOW
        elif score >= 60:
            return RiskLevel.MEDIUM
        elif score >= 40:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def _identify_gaps(
        self,
        controls: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Identify compliance gaps from control results."""
        gaps = []
        
        for control in controls:
            if control.get("status") in ["fail", "needs_review"]:
                control_gaps = control.get("gaps", [])
                severity = "critical" if control.get("status") == "fail" else "medium"
                
                for gap in control_gaps:
                    gaps.append({
                        "control_id": control.get("control_id", ""),
                        "control_title": control.get("title", ""),
                        "gap_description": gap,
                        "severity": severity,
                        "category": control.get("category", ""),
                    })
                
                # Add gap even if no specific gaps listed
                if not control_gaps:
                    gaps.append({
                        "control_id": control.get("control_id", ""),
                        "control_title": control.get("title", ""),
                        "gap_description": f"Control needs attention: {control.get('summary', '')}",
                        "severity": severity,
                        "category": control.get("category", ""),
                    })
        
        return gaps
    
    def _generate_recommendations(
        self,
        category_scores: Dict[str, float],
        gaps: List[Dict[str, Any]],
        compliance_percentage: float,
    ) -> List[str]:
        """Generate prioritized recommendations."""
        recommendations = []
        
        # Find weakest categories
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1],
        )
        
        # Add category-specific recommendations
        for category, score in sorted_categories[:3]:  # Top 3 weakest
            if score < 70:
                recommendations.append(
                    f"🎯 Priority: Improve {category} controls (current score: {score:.0f}%)"
                )
        
        # Add gap-specific recommendations
        critical_gaps = [g for g in gaps if g["severity"] == "critical"]
        if critical_gaps:
            recommendations.append(
                f"🚨 Address {len(critical_gaps)} critical gaps before audit"
            )
        
        # General recommendations based on compliance level
        if compliance_percentage < 50:
            recommendations.extend([
                "📋 Conduct comprehensive policy review",
                "🔧 Implement foundational security controls",
                "📚 Develop employee security training program",
            ])
        elif compliance_percentage < 75:
            recommendations.extend([
                "📝 Document existing procedures formally",
                "🔍 Implement continuous monitoring",
                "🔄 Establish regular access reviews",
            ])
        else:
            recommendations.extend([
                "✅ Maintain current compliance posture",
                "📊 Implement metrics and KPIs tracking",
                "🎓 Continue security awareness training",
            ])
        
        return recommendations[:7]  # Return top 7 recommendations
    
    def _estimate_remediation_time(
        self,
        gaps: List[Dict[str, Any]],
    ) -> int:
        """Estimate total remediation time in hours."""
        total_hours = 0
        
        for gap in gaps:
            description = gap.get("gap_description", "").lower()
            
            # Estimate based on gap type
            if any(word in description for word in ["policy", "document"]):
                total_hours += REMEDIATION_HOURS["policy"]
            elif any(word in description for word in ["procedure", "process"]):
                total_hours += REMEDIATION_HOURS["procedure"]
            elif any(word in description for word in ["implement", "deploy", "configure"]):
                total_hours += REMEDIATION_HOURS["technical"]
            elif any(word in description for word in ["training", "awareness"]):
                total_hours += REMEDIATION_HOURS["training"]
            else:
                total_hours += 16  # Default estimate
        
        return total_hours
    
    def _determine_audit_readiness(
        self,
        score: float,
        critical_count: int,
        compliance_pct: float,
    ) -> str:
        """Determine overall audit readiness status."""
        if score >= 85 and critical_count == 0 and compliance_pct >= 90:
            return "Ready"
        elif score >= 70 and critical_count <= 2 and compliance_pct >= 75:
            return "Almost Ready"
        elif score >= 50 and compliance_pct >= 50:
            return "Needs Work"
        else:
            return "Not Ready"


# Singleton instance
_risk_calculator: RiskCalculator | None = None


def get_risk_calculator() -> RiskCalculator:
    """Get or create risk calculator instance."""
    global _risk_calculator
    if _risk_calculator is None:
        _risk_calculator = RiskCalculator()
    return _risk_calculator
