#!/usr/bin/env python3
"""
ShieldAgent SOC 2 Compliance Demo Script

This script demonstrates the SOC 2 compliance checking capabilities
without requiring the full Docker setup.

Usage:
    python demo_soc2_analysis.py [--scan-type quick|full]
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_section(title: str):
    """Print a section header."""
    print(f"\n📌 {title}")
    print("-" * 40)


def get_risk_emoji(level: str) -> str:
    """Get emoji for risk level."""
    return {
        "minimal": "🟢",
        "low": "🟡",
        "medium": "🟠",
        "high": "🔴",
        "critical": "⚫",
    }.get(level.lower(), "⚪")


def get_status_emoji(status: str) -> str:
    """Get emoji for control status."""
    return {
        "pass": "✅",
        "fail": "❌",
        "needs_review": "⚠️",
        "error": "💥",
    }.get(status.lower(), "❓")


async def run_demo(scan_type: str = "quick"):
    """Run the SOC 2 compliance demo."""
    print_header("🛡️  ShieldAgent SOC 2 Compliance Demo")
    print(f"\n📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔍 Scan Type: {scan_type.upper()}")
    
    # Check for Gemini API key
    from core.config import settings
    
    if not settings.gemini_api_key or settings.gemini_api_key == "your-gemini-api-key-here":
        print("\n⚠️  Warning: GEMINI_API_KEY not configured!")
        print("   Set the environment variable or update backend/.env")
        print("   Running in DEMO mode with simulated results...\n")
        use_ai = False
    else:
        print(f"\n✅ Gemini API configured (model: {settings.gemini_model})")
        use_ai = True
    
    # Load sample documents
    print_section("Loading Sample Documents")
    
    sample_docs_dir = Path(__file__).parent / "sample_documents"
    documents = []
    
    for doc_file in sample_docs_dir.glob("*"):
        if doc_file.suffix in [".json", ".csv", ".md", ".txt"]:
            documents.append(doc_file)
            print(f"  📄 {doc_file.name}")
    
    print(f"\n  Total: {len(documents)} documents loaded")
    
    # Show available controls
    print_section("SOC 2 Controls Overview")
    
    from services.soc2_controls import (
        get_all_controls,
        get_quick_scan_controls,
        get_control_categories,
        CONTROL_SUMMARY,
    )
    
    print(f"\n  📊 Total Controls Available: {CONTROL_SUMMARY['total_controls']}")
    print("\n  By Category:")
    for category, count in CONTROL_SUMMARY["categories"].items():
        print(f"    • {category}: {count} controls")
    
    # Get controls for this scan
    if scan_type == "full":
        controls = get_all_controls()
    else:
        controls = get_quick_scan_controls()
    
    print(f"\n  🎯 Controls in this scan: {len(controls)}")
    
    # Run analysis
    print_section("Running Compliance Analysis")
    
    if use_ai:
        # Use actual Gemini service
        from services.gemini_service import GeminiService
        
        gemini = GeminiService(scan_type=scan_type)
        doc_paths = [str(d) for d in documents]
        
        print("\n  Analyzing documents against controls...")
        print("  This may take a few minutes...\n")
        
        def progress_callback(current, total, control_id):
            pct = int((current / total) * 100)
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            print(f"\r  [{bar}] {pct}% - {control_id}", end="", flush=True)
        
        results = await gemini.analyze_documents(doc_paths, progress_callback)
        print("\n")
    else:
        # Generate demo results
        results = generate_demo_results(controls)
    
    # Calculate risk score
    print_section("Risk Assessment")
    
    from services.risk_calculator import RiskCalculator
    
    calculator = RiskCalculator()
    
    # Format results for risk calculator
    formatted_results = {
        "controls": [
            {
                "control_id": e["control_id"],
                "status": e["status"],
                "confidence": e.get("confidence", 0.8),
                "summary": e.get("summary", ""),
                "category": get_control_category(e["control_id"], controls),
                "title": get_control_title(e["control_id"], controls),
                "gaps": [],
            }
            for e in results["evidence_items"]
        ]
    }
    
    risk_score = calculator.calculate_risk_score(formatted_results)
    
    print(f"\n  {get_risk_emoji(risk_score.risk_level.value)} Overall Risk Level: {risk_score.risk_level.value.upper()}")
    print(f"  📈 Compliance Score: {risk_score.overall_score:.1f}/100")
    print(f"  ✅ Compliance Rate: {risk_score.compliance_percentage:.1f}%")
    print(f"  🚨 Gap Count: {risk_score.gap_count}")
    print(f"  🎯 Audit Readiness: {risk_score.audit_readiness}")
    
    # Category breakdown
    print_section("Category Scores")
    
    for category, score in sorted(risk_score.category_scores.items(), key=lambda x: x[1]):
        bar_length = int(score / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        emoji = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
        print(f"  {emoji} {category:25} [{bar}] {score:.0f}%")
    
    # Control results summary
    print_section("Control Results Summary")
    
    passing = sum(1 for e in results["evidence_items"] if e["status"] == "pass")
    failing = sum(1 for e in results["evidence_items"] if e["status"] == "fail")
    review = sum(1 for e in results["evidence_items"] if e["status"] == "needs_review")
    
    total = len(results["evidence_items"])
    print(f"\n  ✅ Passing:      {passing:3} ({passing/total*100:.0f}%)")
    print(f"  ❌ Failing:      {failing:3} ({failing/total*100:.0f}%)")
    print(f"  ⚠️  Needs Review: {review:3} ({review/total*100:.0f}%)")
    
    # Detailed control results
    print_section("Detailed Control Results")
    
    for evidence in results["evidence_items"][:15]:  # Show first 15
        status = get_status_emoji(evidence["status"])
        confidence = evidence.get("confidence", 0) * 100
        print(f"\n  {status} {evidence['control_id']}: {get_control_title(evidence['control_id'], controls)}")
        print(f"     Confidence: {confidence:.0f}%")
        if evidence.get("summary"):
            summary = evidence["summary"][:100] + "..." if len(evidence.get("summary", "")) > 100 else evidence.get("summary", "")
            print(f"     Summary: {summary}")
    
    if len(results["evidence_items"]) > 15:
        print(f"\n  ... and {len(results['evidence_items']) - 15} more controls")
    
    # Recommendations
    print_section("Recommendations")
    
    for i, rec in enumerate(risk_score.recommendations[:5], 1):
        print(f"  {i}. {rec}")
    
    # Estimated effort
    print_section("Remediation Estimate")
    
    hours = risk_score.estimated_remediation_hours
    days = hours / 8
    print(f"\n  ⏱️  Estimated Effort: {hours} hours ({days:.1f} business days)")
    
    # Summary
    print_header("📋 Executive Summary")
    
    print(f"""
  Organization assessed against SOC 2 Trust Service Criteria
  
  • Controls Evaluated: {len(controls)}
  • Documents Analyzed: {len(documents)}
  • Overall Score: {risk_score.overall_score:.1f}/100
  • Risk Level: {risk_score.risk_level.value.upper()}
  • Audit Readiness: {risk_score.audit_readiness}
  
  Key Findings:
  • {passing} controls passing ({passing/total*100:.0f}%)
  • {failing} controls failing ({failing/total*100:.0f}%)
  • {review} controls need review ({review/total*100:.0f}%)
  • {len(risk_score.critical_gaps)} critical gaps identified
  
  Recommended Next Steps:
  1. Address {len(risk_score.critical_gaps)} critical gaps immediately
  2. Review and remediate {failing} failing controls
  3. Complete evidence for {review} controls needing review
  4. Estimated {hours} hours of remediation work
    """)
    
    print("=" * 60)
    print("  🛡️  ShieldAgent - AI-Powered SOC 2 Compliance")
    print("=" * 60 + "\n")


def get_control_category(control_id: str, controls: list) -> str:
    """Get category for a control ID."""
    for c in controls:
        if c["control_id"] == control_id:
            return c["category"]
    return "Security"


def get_control_title(control_id: str, controls: list) -> str:
    """Get title for a control ID."""
    for c in controls:
        if c["control_id"] == control_id:
            return c["title"]
    return control_id


def generate_demo_results(controls: list) -> dict:
    """Generate demo results for when Gemini API is not available."""
    import random
    
    # Seed for reproducible results
    random.seed(42)
    
    evidence_items = []
    
    for control in controls:
        # Simulate realistic results based on control type
        control_id = control["control_id"]
        
        # Most common controls are more likely to pass in demo
        if control_id in ["CC6.1", "CC6.2", "CC6.3", "CC7.2", "CC8.1"]:
            status = random.choices(["pass", "needs_review", "fail"], weights=[0.7, 0.2, 0.1])[0]
        else:
            status = random.choices(["pass", "needs_review", "fail"], weights=[0.6, 0.25, 0.15])[0]
        
        confidence = random.uniform(0.7, 0.95) if status == "pass" else random.uniform(0.5, 0.8)
        
        summaries = {
            "pass": f"Evidence found supporting {control['title']}. Documentation appears adequate.",
            "needs_review": f"Partial evidence found for {control['title']}. Manual review recommended.",
            "fail": f"Insufficient evidence for {control['title']}. Gap identified.",
        }
        
        evidence_items.append({
            "control_id": control_id,
            "status": status,
            "confidence": confidence,
            "summary": summaries[status],
            "evidence_quote": None,
        })
    
    passing = sum(1 for e in evidence_items if e["status"] == "pass")
    failing = sum(1 for e in evidence_items if e["status"] == "fail")
    review = sum(1 for e in evidence_items if e["status"] == "needs_review")
    
    return {
        "evidence_items": evidence_items,
        "gaps": [],
        "summary": {
            "total_controls": len(controls),
            "passing": passing,
            "failing": failing,
            "needs_review": review,
        }
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ShieldAgent SOC 2 Compliance Demo")
    parser.add_argument(
        "--scan-type",
        choices=["quick", "full"],
        default="quick",
        help="Scan type: 'quick' for 8 key controls, 'full' for all 50+ controls"
    )
    
    args = parser.parse_args()
    
    # Set environment variables for demo
    os.environ.setdefault("DATABASE_URL", "sqlite:///./demo.db")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
    
    asyncio.run(run_demo(args.scan_type))
