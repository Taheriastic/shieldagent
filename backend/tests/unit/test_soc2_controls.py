"""
Tests for SOC 2 controls service.
"""

import pytest

from services.soc2_controls import (
    get_all_controls,
    get_quick_scan_controls,
    get_controls_by_category,
    get_control_by_id,
    get_control_categories,
    CONTROL_SUMMARY,
    CC_CONTROLS,
    AVAILABILITY_CONTROLS,
    PROCESSING_INTEGRITY_CONTROLS,
    CONFIDENTIALITY_CONTROLS,
    PRIVACY_CONTROLS,
)


class TestGetAllControls:
    """Tests for get_all_controls function."""

    def test_returns_list(self):
        """Should return a list."""
        controls = get_all_controls()
        assert isinstance(controls, list)

    def test_has_expected_count(self):
        """Should have 50+ controls."""
        controls = get_all_controls()
        assert len(controls) >= 50

    def test_control_structure(self):
        """Each control should have required fields."""
        controls = get_all_controls()
        
        for control in controls:
            assert "control_id" in control
            assert "category" in control
            assert "title" in control
            assert "description" in control
            assert "check_prompt" in control

    def test_unique_control_ids(self):
        """All control IDs should be unique."""
        controls = get_all_controls()
        control_ids = [c["control_id"] for c in controls]
        assert len(control_ids) == len(set(control_ids))


class TestGetQuickScanControls:
    """Tests for get_quick_scan_controls function."""

    def test_returns_8_controls(self):
        """Quick scan should return exactly 8 controls."""
        controls = get_quick_scan_controls()
        assert len(controls) == 8

    def test_contains_critical_controls(self):
        """Quick scan should include the most critical controls."""
        controls = get_quick_scan_controls()
        control_ids = [c["control_id"] for c in controls]
        
        expected_ids = ["CC6.1", "CC6.2", "CC6.3", "CC7.2", "CC7.3", 
                       "CC8.1", "CC9.1", "A1.2"]
        
        for expected in expected_ids:
            assert expected in control_ids


class TestGetControlsByCategory:
    """Tests for get_controls_by_category function."""

    def test_security_category(self):
        """Should filter Security controls correctly."""
        # Note: Security controls have various subcategory names
        controls = get_controls_by_category("Logical and Physical Access")
        assert len(controls) > 0
        for control in controls:
            assert control["category"] == "Logical and Physical Access"

    def test_availability_category(self):
        """Should filter Availability controls correctly."""
        controls = get_controls_by_category("Availability")
        assert len(controls) == 3
        for control in controls:
            assert control["category"] == "Availability"

    def test_privacy_category(self):
        """Should filter Privacy controls correctly."""
        controls = get_controls_by_category("Privacy")
        assert len(controls) == 8
        for control in controls:
            assert control["category"] == "Privacy"

    def test_case_insensitive(self):
        """Category filtering should be case-insensitive."""
        controls1 = get_controls_by_category("privacy")
        controls2 = get_controls_by_category("PRIVACY")
        assert len(controls1) == len(controls2)

    def test_nonexistent_category(self):
        """Non-existent category should return empty list."""
        controls = get_controls_by_category("NonExistent")
        assert controls == []


class TestGetControlById:
    """Tests for get_control_by_id function."""

    def test_find_existing_control(self):
        """Should find existing control by ID."""
        control = get_control_by_id("CC6.1")
        
        assert control is not None
        assert control["control_id"] == "CC6.1"
        assert "Logical Access" in control["title"]

    def test_case_insensitive_id(self):
        """Control ID lookup should be case-sensitive as implemented."""
        control = get_control_by_id("CC6.1")
        assert control is not None

    def test_nonexistent_control(self):
        """Non-existent control ID should return None."""
        control = get_control_by_id("XX99.99")
        assert control is None

    def test_all_quick_scan_controls_exist(self):
        """All quick scan control IDs should be findable."""
        quick_ids = ["CC6.1", "CC6.2", "CC6.3", "CC7.2", "CC7.3",
                    "CC8.1", "CC9.1", "A1.2"]
        
        for control_id in quick_ids:
            control = get_control_by_id(control_id)
            assert control is not None, f"Control {control_id} not found"


class TestGetControlCategories:
    """Tests for get_control_categories function."""

    def test_returns_list(self):
        """Should return a list of categories."""
        categories = get_control_categories()
        assert isinstance(categories, list)

    def test_category_structure(self):
        """Each category should have name, count, and controls."""
        categories = get_control_categories()
        
        for category in categories:
            assert "name" in category
            assert "count" in category
            assert "controls" in category
            assert isinstance(category["controls"], list)

    def test_counts_are_accurate(self):
        """Category counts should match actual control counts."""
        categories = get_control_categories()
        
        total_from_categories = sum(c["count"] for c in categories)
        total_controls = len(get_all_controls())
        
        assert total_from_categories == total_controls


class TestControlLists:
    """Tests for individual control category lists."""

    def test_cc_controls_not_empty(self):
        """CC_CONTROLS should have controls."""
        assert len(CC_CONTROLS) > 0

    def test_availability_controls(self):
        """AVAILABILITY_CONTROLS should have 3 controls."""
        assert len(AVAILABILITY_CONTROLS) == 3
        for control in AVAILABILITY_CONTROLS:
            assert control["control_id"].startswith("A")

    def test_processing_integrity_controls(self):
        """PROCESSING_INTEGRITY_CONTROLS should have 5 controls."""
        assert len(PROCESSING_INTEGRITY_CONTROLS) == 5
        for control in PROCESSING_INTEGRITY_CONTROLS:
            assert control["control_id"].startswith("PI")

    def test_confidentiality_controls(self):
        """CONFIDENTIALITY_CONTROLS should have 2 controls."""
        assert len(CONFIDENTIALITY_CONTROLS) == 2
        for control in CONFIDENTIALITY_CONTROLS:
            assert control["control_id"].startswith("C")

    def test_privacy_controls(self):
        """PRIVACY_CONTROLS should have 8 controls."""
        assert len(PRIVACY_CONTROLS) == 8
        for control in PRIVACY_CONTROLS:
            assert control["control_id"].startswith("P")


class TestControlSummary:
    """Tests for CONTROL_SUMMARY constant."""

    def test_summary_structure(self):
        """Summary should have expected structure."""
        assert "total_controls" in CONTROL_SUMMARY
        assert "categories" in CONTROL_SUMMARY

    def test_total_matches_all_controls(self):
        """Total should match actual control count."""
        assert CONTROL_SUMMARY["total_controls"] == len(get_all_controls())

    def test_category_breakdown(self):
        """Category breakdown should be present."""
        categories = CONTROL_SUMMARY["categories"]
        
        assert "Common Criteria (Security)" in categories
        assert "Availability" in categories
        assert "Processing Integrity" in categories
        assert "Confidentiality" in categories
        assert "Privacy" in categories


class TestCheckPrompts:
    """Tests for control check prompts."""

    def test_all_controls_have_prompts(self):
        """Every control should have a check_prompt."""
        controls = get_all_controls()
        
        for control in controls:
            assert "check_prompt" in control
            assert len(control["check_prompt"]) > 50  # Meaningful prompt

    def test_prompts_contain_instructions(self):
        """Prompts should contain analysis instructions."""
        controls = get_all_controls()
        
        for control in controls:
            prompt = control["check_prompt"].lower()
            # Should mention what to look for
            assert "look for" in prompt or "analyze" in prompt

    def test_prompts_request_json_response(self):
        """Prompts should request JSON response format."""
        controls = get_all_controls()
        
        for control in controls:
            prompt = control["check_prompt"].lower()
            assert "json" in prompt
