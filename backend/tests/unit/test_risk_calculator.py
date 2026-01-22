"""
Tests for risk calculator service.
"""

import pytest

from services.risk_calculator import (
    RiskCalculator,
    RiskLevel,
    RiskScore,
    CATEGORY_WEIGHTS,
)


@pytest.fixture
def calculator():
    """Create a risk calculator instance."""
    return RiskCalculator()


@pytest.fixture
def sample_passing_results():
    """Sample results where most controls pass."""
    return {
        "controls": [
            {
                "control_id": "CC6.1",
                "category": "Logical and Physical Access",
                "title": "Logical Access Security",
                "status": "pass",
                "confidence": 0.95,
                "gaps": [],
            },
            {
                "control_id": "CC6.2",
                "category": "Logical and Physical Access",
                "title": "User Registration",
                "status": "pass",
                "confidence": 0.90,
                "gaps": [],
            },
            {
                "control_id": "CC7.2",
                "category": "System Operations",
                "title": "Security Monitoring",
                "status": "pass",
                "confidence": 0.85,
                "gaps": [],
            },
            {
                "control_id": "CC8.1",
                "category": "Change Management",
                "title": "Change Management Process",
                "status": "pass",
                "confidence": 0.88,
                "gaps": [],
            },
            {
                "control_id": "A1.2",
                "category": "Availability",
                "title": "Backup and Recovery",
                "status": "pass",
                "confidence": 0.92,
                "gaps": [],
            },
        ]
    }


@pytest.fixture
def sample_failing_results():
    """Sample results where most controls fail."""
    return {
        "controls": [
            {
                "control_id": "CC6.1",
                "category": "Logical and Physical Access",
                "title": "Logical Access Security",
                "status": "fail",
                "confidence": 0.80,
                "gaps": ["No MFA implemented", "Missing access reviews"],
            },
            {
                "control_id": "CC7.2",
                "category": "System Operations",
                "title": "Security Monitoring",
                "status": "fail",
                "confidence": 0.75,
                "gaps": ["No SIEM deployed"],
            },
            {
                "control_id": "A1.2",
                "category": "Availability",
                "title": "Backup and Recovery",
                "status": "fail",
                "confidence": 0.70,
                "gaps": ["No backup testing", "No DR plan"],
            },
        ]
    }


@pytest.fixture
def sample_mixed_results():
    """Sample results with mixed pass/fail/review statuses."""
    return {
        "controls": [
            {
                "control_id": "CC6.1",
                "category": "Logical and Physical Access",
                "title": "Logical Access Security",
                "status": "pass",
                "confidence": 0.90,
                "gaps": [],
            },
            {
                "control_id": "CC6.2",
                "category": "Logical and Physical Access",
                "title": "User Registration",
                "status": "needs_review",
                "confidence": 0.60,
                "gaps": ["Incomplete documentation"],
            },
            {
                "control_id": "CC7.2",
                "category": "System Operations",
                "title": "Security Monitoring",
                "status": "fail",
                "confidence": 0.85,
                "gaps": ["No 24/7 monitoring"],
            },
            {
                "control_id": "A1.2",
                "category": "Availability",
                "title": "Backup and Recovery",
                "status": "pass",
                "confidence": 0.88,
                "gaps": [],
            },
        ]
    }


class TestRiskCalculatorBasics:
    """Basic tests for RiskCalculator."""

    def test_calculator_initialization(self, calculator):
        """Calculator should initialize properly."""
        assert calculator is not None

    def test_empty_results(self, calculator):
        """Empty results should return critical risk."""
        result = calculator.calculate_risk_score({"controls": []})
        
        assert isinstance(result, RiskScore)
        assert result.risk_level == RiskLevel.CRITICAL
        assert result.overall_score == 0
        assert result.audit_readiness == "Not Ready"

    def test_missing_controls_key(self, calculator):
        """Missing controls key should return critical risk."""
        result = calculator.calculate_risk_score({})
        
        assert result.risk_level == RiskLevel.CRITICAL


class TestRiskScoreCalculation:
    """Tests for risk score calculation."""

    def test_passing_results_high_score(
        self, calculator, sample_passing_results
    ):
        """Passing results should yield high score."""
        result = calculator.calculate_risk_score(sample_passing_results)
        
        assert result.overall_score >= 70
        assert result.risk_level in [RiskLevel.MINIMAL, RiskLevel.LOW]
        assert result.compliance_percentage == 100.0

    def test_failing_results_low_score(
        self, calculator, sample_failing_results
    ):
        """Failing results should yield low score."""
        result = calculator.calculate_risk_score(sample_failing_results)
        
        assert result.overall_score < 50
        assert result.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
        assert result.compliance_percentage == 0.0
        assert result.gap_count > 0

    def test_mixed_results_medium_score(
        self, calculator, sample_mixed_results
    ):
        """Mixed results should yield medium score."""
        result = calculator.calculate_risk_score(sample_mixed_results)
        
        assert 30 <= result.overall_score <= 80
        assert result.compliance_percentage == 50.0  # 2 out of 4 passing


class TestRiskLevelDetermination:
    """Tests for risk level determination."""

    def test_minimal_risk_threshold(self, calculator):
        """Score >= 90 should be minimal risk."""
        # Create all passing controls with high confidence
        results = {
            "controls": [
                {
                    "control_id": f"CC{i}.1",
                    "category": "Security",
                    "title": f"Control {i}",
                    "status": "pass",
                    "confidence": 0.99,
                    "gaps": [],
                }
                for i in range(10)
            ]
        }
        
        result = calculator.calculate_risk_score(results)
        assert result.risk_level == RiskLevel.MINIMAL

    def test_critical_risk_threshold(self, calculator, sample_failing_results):
        """Very low scores should be critical risk."""
        result = calculator.calculate_risk_score(sample_failing_results)
        
        # All failing should give critical or high
        assert result.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]


class TestCategoryScores:
    """Tests for category score calculation."""

    def test_category_scores_present(
        self, calculator, sample_passing_results
    ):
        """Category scores should be calculated."""
        result = calculator.calculate_risk_score(sample_passing_results)
        
        assert len(result.category_scores) > 0

    def test_category_weights_applied(self):
        """Category weights should be defined."""
        assert "Security" in CATEGORY_WEIGHTS
        assert "Availability" in CATEGORY_WEIGHTS
        assert sum(CATEGORY_WEIGHTS.values()) == 1.0


class TestGapIdentification:
    """Tests for gap identification."""

    def test_gaps_identified_from_failures(
        self, calculator, sample_failing_results
    ):
        """Gaps should be identified from failing controls."""
        result = calculator.calculate_risk_score(sample_failing_results)
        
        assert result.gap_count > 0

    def test_critical_gaps_identified(
        self, calculator, sample_failing_results
    ):
        """Critical gaps should be extracted."""
        result = calculator.calculate_risk_score(sample_failing_results)
        
        # Failing controls should produce critical gaps
        assert isinstance(result.critical_gaps, list)

    def test_no_gaps_for_passing(
        self, calculator, sample_passing_results
    ):
        """Passing controls should have no gaps."""
        result = calculator.calculate_risk_score(sample_passing_results)
        
        assert result.gap_count == 0
        assert len(result.critical_gaps) == 0


class TestRecommendations:
    """Tests for recommendation generation."""

    def test_recommendations_generated(
        self, calculator, sample_mixed_results
    ):
        """Recommendations should be generated."""
        result = calculator.calculate_risk_score(sample_mixed_results)
        
        assert len(result.recommendations) > 0

    def test_recommendations_are_strings(
        self, calculator, sample_mixed_results
    ):
        """All recommendations should be strings."""
        result = calculator.calculate_risk_score(sample_mixed_results)
        
        for rec in result.recommendations:
            assert isinstance(rec, str)
            assert len(rec) > 10  # Meaningful recommendation


class TestRemediationEstimate:
    """Tests for remediation time estimation."""

    def test_remediation_hours_calculated(
        self, calculator, sample_failing_results
    ):
        """Remediation hours should be estimated."""
        result = calculator.calculate_risk_score(sample_failing_results)
        
        assert result.estimated_remediation_hours > 0

    def test_no_remediation_for_passing(
        self, calculator, sample_passing_results
    ):
        """Passing results should have minimal remediation."""
        result = calculator.calculate_risk_score(sample_passing_results)
        
        assert result.estimated_remediation_hours == 0


class TestAuditReadiness:
    """Tests for audit readiness determination."""

    def test_ready_status(self, calculator, sample_passing_results):
        """High scores should be audit ready."""
        result = calculator.calculate_risk_score(sample_passing_results)
        
        assert result.audit_readiness in ["Ready", "Almost Ready"]

    def test_not_ready_status(self, calculator, sample_failing_results):
        """Low scores should not be audit ready."""
        result = calculator.calculate_risk_score(sample_failing_results)
        
        assert result.audit_readiness in ["Not Ready", "Needs Work"]

    def test_valid_readiness_values(self, calculator, sample_mixed_results):
        """Audit readiness should be a valid value."""
        result = calculator.calculate_risk_score(sample_mixed_results)
        
        valid_values = ["Ready", "Almost Ready", "Needs Work", "Not Ready"]
        assert result.audit_readiness in valid_values
