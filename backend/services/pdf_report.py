"""
PDF Report Generation Service for SOC 2 Compliance Reports.
Creates professional, branded compliance reports.
"""

from io import BytesIO
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class PDFReportGenerator:
    """Generate professional SOC 2 compliance PDF reports."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Set up custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1e40af'),
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#6b7280'),
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#1e40af'),
        ))
        
        # Control ID style
        self.styles.add(ParagraphStyle(
            name='ControlID',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#4f46e5'),
        ))
        
        # Pass style
        self.styles.add(ParagraphStyle(
            name='StatusPass',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#059669'),
            fontName='Helvetica-Bold',
        ))
        
        # Fail style
        self.styles.add(ParagraphStyle(
            name='StatusFail',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#dc2626'),
            fontName='Helvetica-Bold',
        ))
        
        # Review style
        self.styles.add(ParagraphStyle(
            name='StatusReview',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#d97706'),
            fontName='Helvetica-Bold',
        ))

    def generate_report(
        self,
        organization_name: str,
        analysis_results: dict[str, Any],
        report_date: datetime = None,
    ) -> BytesIO:
        """
        Generate a complete SOC 2 compliance report.
        
        Args:
            organization_name: Name of the organization
            analysis_results: Results from the compliance analysis
            report_date: Date for the report (defaults to now)
            
        Returns:
            BytesIO buffer containing the PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )
        
        if report_date is None:
            report_date = datetime.now()
        
        story = []
        
        # Cover page
        story.extend(self._create_cover_page(organization_name, report_date))
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary(analysis_results))
        story.append(PageBreak())
        
        # Compliance score breakdown
        story.extend(self._create_score_breakdown(analysis_results))
        story.append(PageBreak())
        
        # Detailed findings
        story.extend(self._create_detailed_findings(analysis_results))
        story.append(PageBreak())
        
        # Gap analysis
        story.extend(self._create_gap_analysis(analysis_results))
        story.append(PageBreak())
        
        # Recommendations
        story.extend(self._create_recommendations(analysis_results))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

    def _create_cover_page(self, org_name: str, report_date: datetime) -> list:
        """Create the cover page."""
        elements = []
        
        # Add spacing at top
        elements.append(Spacer(1, 2 * inch))
        
        # Shield icon (using text as placeholder)
        elements.append(Paragraph("🛡️", ParagraphStyle(
            name='ShieldIcon',
            fontSize=72,
            alignment=TA_CENTER,
        )))
        
        elements.append(Spacer(1, 0.5 * inch))
        
        # Title
        elements.append(Paragraph(
            "SOC 2 Compliance Report",
            self.styles['ReportTitle']
        ))
        
        # Organization name
        elements.append(Paragraph(
            org_name,
            self.styles['ReportSubtitle']
        ))
        
        elements.append(Spacer(1, 0.5 * inch))
        
        # Report info
        elements.append(Paragraph(
            f"Generated: {report_date.strftime('%B %d, %Y at %I:%M %p')}",
            ParagraphStyle(
                name='ReportDate',
                parent=self.styles['Normal'],
                fontSize=11,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#6b7280'),
            )
        ))
        
        elements.append(Spacer(1, 0.3 * inch))
        
        elements.append(Paragraph(
            "Automated Compliance Analysis powered by ShieldAgent AI",
            ParagraphStyle(
                name='PoweredBy',
                parent=self.styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#9ca3af'),
            )
        ))
        
        # Confidential notice
        elements.append(Spacer(1, 2 * inch))
        elements.append(HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor('#e5e7eb'),
        ))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(
            "CONFIDENTIAL - FOR INTERNAL USE ONLY",
            ParagraphStyle(
                name='Confidential',
                parent=self.styles['Normal'],
                fontSize=9,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#ef4444'),
                fontName='Helvetica-Bold',
            )
        ))
        
        return elements

    def _create_executive_summary(self, results: dict) -> list:
        """Create executive summary section."""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1e40af')))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Calculate scores
        total = results.get('total_controls', 0)
        passing = results.get('passing', 0)
        failing = results.get('failing', 0)
        needs_review = results.get('needs_review', 0)
        
        score = round((passing / total) * 100) if total > 0 else 0
        
        # Score summary
        score_color = '#059669' if score >= 80 else '#d97706' if score >= 60 else '#dc2626'
        
        elements.append(Paragraph(
            f"Overall Compliance Score: <font color='{score_color}'><b>{score}%</b></font>",
            ParagraphStyle(
                name='ScoreSummary',
                parent=self.styles['Normal'],
                fontSize=18,
                alignment=TA_CENTER,
                spaceBefore=20,
                spaceAfter=20,
            )
        ))
        
        # Summary table
        summary_data = [
            ['Metric', 'Count', 'Percentage'],
            ['Controls Evaluated', str(total), '100%'],
            ['Passing', str(passing), f'{round(passing/total*100) if total else 0}%'],
            ['Failing', str(failing), f'{round(failing/total*100) if total else 0}%'],
            ['Needs Review', str(needs_review), f'{round(needs_review/total*100) if total else 0}%'],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Key findings
        elements.append(Paragraph("Key Findings", self.styles['Heading3']))
        
        if failing > 0:
            elements.append(Paragraph(
                f"• <font color='#dc2626'><b>{failing} control(s)</b></font> require immediate attention",
                self.styles['Normal']
            ))
        
        if needs_review > 0:
            elements.append(Paragraph(
                f"• <font color='#d97706'><b>{needs_review} control(s)</b></font> need manual review",
                self.styles['Normal']
            ))
        
        if passing > 0:
            elements.append(Paragraph(
                f"• <font color='#059669'><b>{passing} control(s)</b></font> are fully compliant",
                self.styles['Normal']
            ))
        
        return elements

    def _create_score_breakdown(self, results: dict) -> list:
        """Create compliance score breakdown by category."""
        elements = []
        
        elements.append(Paragraph("Compliance by Category", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1e40af')))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Group controls by category
        categories = {}
        for control in results.get('controls', []):
            cat = control.get('category', 'Other')
            if cat not in categories:
                categories[cat] = {'pass': 0, 'fail': 0, 'needs_review': 0}
            status = control.get('status', 'needs_review')
            if status == 'pass':
                categories[cat]['pass'] += 1
            elif status == 'fail':
                categories[cat]['fail'] += 1
            else:
                categories[cat]['needs_review'] += 1
        
        # Create category table
        cat_data = [['Category', 'Pass', 'Fail', 'Review', 'Score']]
        for cat, counts in categories.items():
            total = counts['pass'] + counts['fail'] + counts['needs_review']
            score = round(counts['pass'] / total * 100) if total > 0 else 0
            cat_data.append([
                cat,
                str(counts['pass']),
                str(counts['fail']),
                str(counts['needs_review']),
                f"{score}%"
            ])
        
        cat_table = Table(cat_data, colWidths=[2.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        elements.append(cat_table)
        
        return elements

    def _create_detailed_findings(self, results: dict) -> list:
        """Create detailed findings for each control."""
        elements = []
        
        elements.append(Paragraph("Detailed Control Findings", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1e40af')))
        elements.append(Spacer(1, 0.3 * inch))
        
        for control in results.get('controls', []):
            status = control.get('status', 'needs_review')
            
            # Status color and style
            if status == 'pass':
                status_style = self.styles['StatusPass']
                status_text = "✓ PASS"
                bg_color = colors.HexColor('#ecfdf5')
            elif status == 'fail':
                status_style = self.styles['StatusFail']
                status_text = "✗ FAIL"
                bg_color = colors.HexColor('#fef2f2')
            else:
                status_style = self.styles['StatusReview']
                status_text = "⚠ REVIEW"
                bg_color = colors.HexColor('#fffbeb')
            
            # Control header
            elements.append(Paragraph(
                f"{control.get('control_id', 'N/A')} - {control.get('title', 'Unknown')}",
                self.styles['ControlID']
            ))
            
            elements.append(Paragraph(status_text, status_style))
            elements.append(Spacer(1, 0.1 * inch))
            
            # Summary
            elements.append(Paragraph(
                control.get('summary', 'No summary available.'),
                self.styles['Normal']
            ))
            
            # Evidence if available
            if control.get('evidence_quote'):
                elements.append(Spacer(1, 0.1 * inch))
                elements.append(Paragraph(
                    f"<i>Evidence: \"{control['evidence_quote']}\"</i>",
                    ParagraphStyle(
                        name='Evidence',
                        parent=self.styles['Normal'],
                        fontSize=9,
                        textColor=colors.HexColor('#059669'),
                        leftIndent=20,
                    )
                ))
            
            # Gaps if any
            gaps = control.get('gaps', [])
            if gaps:
                elements.append(Spacer(1, 0.1 * inch))
                for gap in gaps:
                    elements.append(Paragraph(
                        f"• Gap: {gap}",
                        ParagraphStyle(
                            name='Gap',
                            parent=self.styles['Normal'],
                            fontSize=9,
                            textColor=colors.HexColor('#dc2626'),
                            leftIndent=20,
                        )
                    ))
            
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(HRFlowable(
                width="100%",
                thickness=0.5,
                color=colors.HexColor('#e5e7eb'),
            ))
            elements.append(Spacer(1, 0.1 * inch))
        
        return elements

    def _create_gap_analysis(self, results: dict) -> list:
        """Create gap analysis section."""
        elements = []
        
        elements.append(Paragraph("Gap Analysis & Risk Assessment", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1e40af')))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Collect all gaps
        gaps = []
        for control in results.get('controls', []):
            for gap in control.get('gaps', []):
                gaps.append({
                    'control_id': control.get('control_id'),
                    'control_title': control.get('title'),
                    'gap': gap,
                    'severity': 'High' if control.get('status') == 'fail' else 'Medium',
                })
        
        if not gaps:
            elements.append(Paragraph(
                "No significant gaps identified. Continue monitoring for ongoing compliance.",
                self.styles['Normal']
            ))
            return elements
        
        # Gap table
        gap_data = [['Control', 'Gap Description', 'Severity']]
        for gap in gaps:
            gap_data.append([
                gap['control_id'],
                gap['gap'][:80] + ('...' if len(gap['gap']) > 80 else ''),
                gap['severity'],
            ])
        
        gap_table = Table(gap_data, colWidths=[1*inch, 4*inch, 0.8*inch])
        gap_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(gap_table)
        
        return elements

    def _create_recommendations(self, results: dict) -> list:
        """Create recommendations section."""
        elements = []
        
        elements.append(Paragraph("Recommendations & Next Steps", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1e40af')))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Standard recommendations based on findings
        failing = results.get('failing', 0)
        needs_review = results.get('needs_review', 0)
        
        recommendations = []
        
        if failing > 0:
            recommendations.append(
                "<b>Immediate Action Required:</b> Address the failing controls identified in this "
                "report. These represent the highest risk items and should be prioritized."
            )
        
        if needs_review > 0:
            recommendations.append(
                "<b>Manual Review Needed:</b> Controls marked for review require human verification. "
                "Schedule time with your compliance team to assess these items."
            )
        
        recommendations.extend([
            "<b>Document Updates:</b> Ensure all policies and procedures are up to date and "
            "reflect current organizational practices.",
            "<b>Evidence Collection:</b> Maintain ongoing evidence collection for all controls "
            "to support your next audit cycle.",
            "<b>Regular Assessments:</b> Schedule quarterly compliance assessments to track "
            "progress and identify new gaps early.",
            "<b>Training:</b> Conduct security awareness training to ensure all employees "
            "understand their role in maintaining compliance.",
        ])
        
        for i, rec in enumerate(recommendations, 1):
            elements.append(Paragraph(
                f"{i}. {rec}",
                ParagraphStyle(
                    name=f'Rec{i}',
                    parent=self.styles['Normal'],
                    fontSize=10,
                    spaceBefore=10,
                    spaceAfter=5,
                )
            ))
        
        # Footer
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e5e7eb')))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(
            "This report was generated by ShieldAgent - AI-Powered SOC 2 Compliance Automation",
            ParagraphStyle(
                name='Footer',
                parent=self.styles['Normal'],
                fontSize=8,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#9ca3af'),
            )
        ))
        
        return elements


# Singleton instance
_pdf_generator = None


def get_pdf_generator() -> PDFReportGenerator:
    """Get or create PDF generator instance."""
    global _pdf_generator
    if _pdf_generator is None:
        _pdf_generator = PDFReportGenerator()
    return _pdf_generator
