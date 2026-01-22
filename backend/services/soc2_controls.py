"""
Complete SOC 2 Controls - All Trust Service Categories

This module contains all SOC 2 Trust Service Criteria (TSC) organized by category:
- CC: Common Criteria (Security)
- A: Availability
- PI: Processing Integrity  
- C: Confidentiality
- P: Privacy
"""

# =============================================================================
# COMMON CRITERIA (CC) - SECURITY
# =============================================================================

CC_CONTROLS = [
    # CC1: Control Environment
    {
        "control_id": "CC1.1",
        "category": "Control Environment",
        "title": "Demonstrates Commitment to Integrity",
        "description": "The entity demonstrates a commitment to integrity and ethical values.",
        "check_prompt": """Analyze for evidence of commitment to integrity and ethics.
Look for:
- Code of conduct/ethics policy
- Ethics training programs
- Whistleblower/reporting mechanisms
- Disciplinary procedures for violations
- Management tone-at-the-top statements

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC1.2",
        "category": "Control Environment",
        "title": "Board Oversight",
        "description": "The board of directors demonstrates independence from management and exercises oversight.",
        "check_prompt": """Analyze for evidence of board oversight of security.
Look for:
- Board charter/governance documents
- Security reporting to board
- Independent board members
- Audit committee structure
- Regular board security reviews

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC1.3",
        "category": "Control Environment",
        "title": "Organizational Structure",
        "description": "Management establishes structures, reporting lines, and appropriate authorities.",
        "check_prompt": """Analyze for evidence of security organizational structure.
Look for:
- Organization charts
- Security team structure
- CISO/security leadership roles
- Reporting lines
- Defined authorities and responsibilities

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC1.4",
        "category": "Control Environment",
        "title": "Competence Commitment",
        "description": "The entity demonstrates a commitment to attract, develop, and retain competent individuals.",
        "check_prompt": """Analyze for evidence of security competence management.
Look for:
- Security training programs
- Certification requirements
- Hiring criteria for security roles
- Performance evaluations
- Professional development programs

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC1.5",
        "category": "Control Environment",
        "title": "Accountability",
        "description": "The entity holds individuals accountable for their internal control responsibilities.",
        "check_prompt": """Analyze for evidence of security accountability.
Look for:
- Performance metrics for security
- Accountability frameworks
- Security responsibilities in job descriptions
- Consequences for non-compliance
- Regular performance reviews

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },

    # CC2: Communication and Information
    {
        "control_id": "CC2.1",
        "category": "Communication and Information",
        "title": "Internal Information Quality",
        "description": "The entity obtains or generates and uses relevant, quality information.",
        "check_prompt": """Analyze for evidence of information quality management.
Look for:
- Data classification policies
- Information accuracy procedures
- Data validation processes
- Quality assurance programs
- Information governance framework

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC2.2",
        "category": "Communication and Information",
        "title": "Internal Communication",
        "description": "The entity internally communicates information necessary for internal controls.",
        "check_prompt": """Analyze for evidence of internal security communication.
Look for:
- Security awareness programs
- Policy distribution procedures
- Internal security newsletters/updates
- Team meeting documentation
- Communication of security incidents

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC2.3",
        "category": "Communication and Information",
        "title": "External Communication",
        "description": "The entity communicates with external parties regarding matters affecting internal controls.",
        "check_prompt": """Analyze for evidence of external security communication.
Look for:
- Customer security notifications
- Vendor security requirements
- Regulatory communication procedures
- Public security disclosures
- External incident communication

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },

    # CC3: Risk Assessment
    {
        "control_id": "CC3.1",
        "category": "Risk Assessment",
        "title": "Risk Objectives",
        "description": "The entity specifies objectives with sufficient clarity to enable identification of risks.",
        "check_prompt": """Analyze for evidence of clear security objectives.
Look for:
- Documented security objectives
- Security strategy documents
- Risk appetite statements
- Security KPIs/metrics
- Alignment with business objectives

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC3.2",
        "category": "Risk Assessment",
        "title": "Risk Identification",
        "description": "The entity identifies risks to the achievement of its objectives.",
        "check_prompt": """Analyze for evidence of risk identification processes.
Look for:
- Risk assessment methodology
- Threat identification procedures
- Vulnerability assessments
- Risk registers
- Risk identification tools/techniques

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC3.3",
        "category": "Risk Assessment",
        "title": "Fraud Risk",
        "description": "The entity considers the potential for fraud in assessing risks.",
        "check_prompt": """Analyze for evidence of fraud risk consideration.
Look for:
- Fraud risk assessment
- Anti-fraud controls
- Segregation of duties
- Fraud detection mechanisms
- Fraud investigation procedures

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC3.4",
        "category": "Risk Assessment",
        "title": "Change Risk",
        "description": "The entity identifies and assesses changes that could significantly impact internal controls.",
        "check_prompt": """Analyze for evidence of change risk assessment.
Look for:
- Change impact assessments
- New system risk evaluations
- Organizational change reviews
- Technology change risk analysis
- Regulatory change monitoring

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },

    # CC4: Monitoring Activities
    {
        "control_id": "CC4.1",
        "category": "Monitoring Activities",
        "title": "Ongoing Monitoring",
        "description": "The entity selects, develops, and performs ongoing evaluations.",
        "check_prompt": """Analyze for evidence of ongoing security monitoring.
Look for:
- Continuous monitoring programs
- Security metrics dashboards
- Automated monitoring tools
- Regular security reviews
- Performance tracking

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC4.2",
        "category": "Monitoring Activities",
        "title": "Deficiency Communication",
        "description": "The entity evaluates and communicates internal control deficiencies timely.",
        "check_prompt": """Analyze for evidence of deficiency management.
Look for:
- Deficiency tracking systems
- Remediation procedures
- Management reporting
- Escalation procedures
- Corrective action plans

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },

    # CC5: Control Activities
    {
        "control_id": "CC5.1",
        "category": "Control Activities",
        "title": "Control Selection",
        "description": "The entity selects and develops control activities that contribute to risk mitigation.",
        "check_prompt": """Analyze for evidence of control selection processes.
Look for:
- Control frameworks used (NIST, ISO, etc.)
- Control selection criteria
- Risk-based control prioritization
- Control implementation plans
- Control documentation

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC5.2",
        "category": "Control Activities",
        "title": "Technology Controls",
        "description": "The entity selects and develops general control activities over technology.",
        "check_prompt": """Analyze for evidence of technology controls.
Look for:
- IT general controls (ITGC)
- System development controls
- Change management controls
- Access controls
- Operations controls

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC5.3",
        "category": "Control Activities",
        "title": "Policy Implementation",
        "description": "The entity deploys control activities through policies and procedures.",
        "check_prompt": """Analyze for evidence of policy implementation.
Look for:
- Security policies
- Standard operating procedures
- Policy review schedules
- Policy acknowledgment records
- Procedure documentation

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },

    # CC6: Logical and Physical Access Controls
    {
        "control_id": "CC6.1",
        "category": "Logical and Physical Access",
        "title": "Logical Access Security",
        "description": "The entity implements logical access security over protected information assets.",
        "check_prompt": """Analyze for evidence of logical access security controls.
Look for:
- Authentication mechanisms (passwords, MFA, SSO)
- Access control lists or role-based access control (RBAC)
- User provisioning and deprovisioning procedures
- Access review processes
- Privileged access management

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC6.2",
        "category": "Logical and Physical Access",
        "title": "User Registration",
        "description": "Prior to issuing credentials, the entity registers and authorizes new users.",
        "check_prompt": """Analyze for evidence of user registration procedures.
Look for:
- New user onboarding procedures
- Authorization approval workflows
- Background check requirements
- System access request forms
- Manager approval requirements

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC6.3",
        "category": "Logical and Physical Access",
        "title": "Access Removal",
        "description": "The entity removes access when no longer required.",
        "check_prompt": """Analyze for evidence of access removal procedures.
Look for:
- Termination procedures for access removal
- Transfer/role change access review
- Timely revocation of access
- Periodic access reviews
- Automated deprovisioning

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC6.4",
        "category": "Logical and Physical Access",
        "title": "Access Restrictions",
        "description": "The entity restricts physical access to facilities and protected assets.",
        "check_prompt": """Analyze for evidence of physical access restrictions.
Look for:
- Physical access controls (badges, biometrics)
- Visitor management procedures
- Data center security
- Secure areas identification
- Physical access logs

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC6.5",
        "category": "Logical and Physical Access",
        "title": "Asset Disposal",
        "description": "The entity discontinues logical and physical protections over assets only after disposition.",
        "check_prompt": """Analyze for evidence of asset disposal procedures.
Look for:
- Data destruction policies
- Media sanitization procedures
- Hardware disposal processes
- Certificate of destruction
- Disposal tracking

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC6.6",
        "category": "Logical and Physical Access",
        "title": "System Boundaries",
        "description": "The entity implements logical access security measures to protect against threats.",
        "check_prompt": """Analyze for evidence of system boundary protection.
Look for:
- Network segmentation
- Firewall configurations
- DMZ architecture
- VPN requirements
- Boundary protection devices

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC6.7",
        "category": "Logical and Physical Access",
        "title": "Information Transmission",
        "description": "The entity restricts transmission of information to authorized users.",
        "check_prompt": """Analyze for evidence of secure data transmission.
Look for:
- Encryption in transit (TLS/SSL)
- Secure file transfer procedures
- Email security controls
- Data loss prevention (DLP)
- Secure communication channels

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC6.8",
        "category": "Logical and Physical Access",
        "title": "Malicious Software Prevention",
        "description": "The entity implements controls to prevent malicious software.",
        "check_prompt": """Analyze for evidence of malware prevention.
Look for:
- Antivirus/anti-malware solutions
- Endpoint protection
- Email filtering
- Web filtering
- Malware detection procedures

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },

    # CC7: System Operations
    {
        "control_id": "CC7.1",
        "category": "System Operations",
        "title": "Vulnerability Detection",
        "description": "The entity detects and monitors configuration and vulnerabilities.",
        "check_prompt": """Analyze for evidence of vulnerability management.
Look for:
- Vulnerability scanning procedures
- Penetration testing
- Configuration management
- Patch management
- Vulnerability remediation

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC7.2",
        "category": "System Operations",
        "title": "Security Monitoring",
        "description": "The entity monitors system components for anomalies indicative of security events.",
        "check_prompt": """Analyze for evidence of security monitoring.
Look for:
- Security monitoring tools (SIEM, IDS/IPS)
- Log collection and analysis
- Alerting thresholds and procedures
- 24/7 monitoring capabilities
- Incident detection procedures

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC7.3",
        "category": "System Operations",
        "title": "Incident Response",
        "description": "The entity evaluates security events and takes actions to address failures.",
        "check_prompt": """Analyze for evidence of incident response procedures.
Look for:
- Incident response plan/playbooks
- Incident classification and severity levels
- Response team roles and responsibilities
- Communication procedures
- Post-incident review process

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC7.4",
        "category": "System Operations",
        "title": "Incident Response Activities",
        "description": "The entity responds to identified security incidents.",
        "check_prompt": """Analyze for evidence of incident response activities.
Look for:
- Containment procedures
- Eradication procedures
- Recovery procedures
- Evidence preservation
- Incident documentation

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC7.5",
        "category": "System Operations",
        "title": "Incident Recovery",
        "description": "The entity identifies, develops, and implements activities to recover from incidents.",
        "check_prompt": """Analyze for evidence of incident recovery capabilities.
Look for:
- Recovery procedures
- Business continuity plans
- Disaster recovery testing
- Recovery time objectives
- Lessons learned process

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },

    # CC8: Change Management
    {
        "control_id": "CC8.1",
        "category": "Change Management",
        "title": "Change Management Process",
        "description": "The entity authorizes, designs, develops, configures, tests, and implements changes.",
        "check_prompt": """Analyze for evidence of change management processes.
Look for:
- Change request procedures
- Change approval workflows
- Testing requirements before deployment
- Documentation requirements
- Rollback procedures

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },

    # CC9: Risk Mitigation
    {
        "control_id": "CC9.1",
        "category": "Risk Mitigation",
        "title": "Risk Mitigation Activities",
        "description": "The entity identifies and develops risk mitigation activities.",
        "check_prompt": """Analyze for evidence of risk mitigation processes.
Look for:
- Risk assessment methodology
- Risk identification procedures
- Risk rating/scoring criteria
- Risk treatment plans
- Regular risk review schedule

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "CC9.2",
        "category": "Risk Mitigation",
        "title": "Vendor Risk Management",
        "description": "The entity assesses and manages risks associated with vendors.",
        "check_prompt": """Analyze for evidence of vendor risk management.
Look for:
- Vendor assessment procedures
- Due diligence processes
- Contract security requirements
- Ongoing vendor monitoring
- Vendor risk ratings

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
]

# =============================================================================
# AVAILABILITY (A) CRITERIA
# =============================================================================

AVAILABILITY_CONTROLS = [
    {
        "control_id": "A1.1",
        "category": "Availability",
        "title": "Capacity Planning",
        "description": "The entity maintains, monitors, and evaluates current processing capacity.",
        "check_prompt": """Analyze for evidence of capacity planning.
Look for:
- Capacity monitoring procedures
- Performance baselines
- Scalability planning
- Resource utilization metrics
- Capacity forecasting

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "A1.2",
        "category": "Availability",
        "title": "Backup and Recovery",
        "description": "The entity implements environmental protections and recovery infrastructure.",
        "check_prompt": """Analyze for evidence of backup and recovery procedures.
Look for:
- Backup policies and schedules
- Backup testing/verification
- Recovery time objectives (RTO)
- Recovery point objectives (RPO)
- Disaster recovery procedures

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "A1.3",
        "category": "Availability",
        "title": "Recovery Plan Testing",
        "description": "The entity tests recovery plan procedures supporting system recovery.",
        "check_prompt": """Analyze for evidence of recovery plan testing.
Look for:
- DR test schedules
- Test scenarios and results
- Recovery time achievements
- Lessons learned documentation
- Plan updates based on testing

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
]

# =============================================================================
# PROCESSING INTEGRITY (PI) CRITERIA
# =============================================================================

PROCESSING_INTEGRITY_CONTROLS = [
    {
        "control_id": "PI1.1",
        "category": "Processing Integrity",
        "title": "Data Processing Objectives",
        "description": "The entity obtains and documents processing requirements.",
        "check_prompt": """Analyze for evidence of processing integrity objectives.
Look for:
- Data processing specifications
- Input validation requirements
- Processing accuracy standards
- Output verification procedures
- Data quality objectives

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "PI1.2",
        "category": "Processing Integrity",
        "title": "Input Controls",
        "description": "The entity implements policies for accuracy and completeness of inputs.",
        "check_prompt": """Analyze for evidence of input controls.
Look for:
- Input validation procedures
- Data entry controls
- Error handling procedures
- Data completeness checks
- Authorization of inputs

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "PI1.3",
        "category": "Processing Integrity",
        "title": "Processing Controls",
        "description": "The entity implements policies for complete and accurate processing.",
        "check_prompt": """Analyze for evidence of processing controls.
Look for:
- Processing accuracy verification
- Reconciliation procedures
- Error detection mechanisms
- Processing monitoring
- Transaction logging

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "PI1.4",
        "category": "Processing Integrity",
        "title": "Output Controls",
        "description": "The entity implements policies for protecting outputs.",
        "check_prompt": """Analyze for evidence of output controls.
Look for:
- Output validation procedures
- Distribution controls
- Output retention policies
- Output integrity verification
- Authorized recipients

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "PI1.5",
        "category": "Processing Integrity",
        "title": "Data Retention",
        "description": "The entity retains information in accordance with objectives.",
        "check_prompt": """Analyze for evidence of data retention policies.
Look for:
- Retention schedules
- Legal hold procedures
- Archive procedures
- Destruction schedules
- Retention compliance

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
]

# =============================================================================
# CONFIDENTIALITY (C) CRITERIA
# =============================================================================

CONFIDENTIALITY_CONTROLS = [
    {
        "control_id": "C1.1",
        "category": "Confidentiality",
        "title": "Confidential Information Identification",
        "description": "The entity identifies and maintains confidential information.",
        "check_prompt": """Analyze for evidence of confidential information management.
Look for:
- Data classification policies
- Confidential data inventory
- Classification labeling
- Handling procedures by classification
- Classification training

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "C1.2",
        "category": "Confidentiality",
        "title": "Confidential Information Disposal",
        "description": "The entity disposes of confidential information according to objectives.",
        "check_prompt": """Analyze for evidence of confidential data disposal.
Look for:
- Secure disposal procedures
- Media sanitization
- Certificate of destruction
- Disposal verification
- Third-party disposal oversight

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
]

# =============================================================================
# PRIVACY (P) CRITERIA
# =============================================================================

PRIVACY_CONTROLS = [
    {
        "control_id": "P1.1",
        "category": "Privacy",
        "title": "Privacy Notice",
        "description": "The entity provides notice about its privacy practices.",
        "check_prompt": """Analyze for evidence of privacy notice practices.
Look for:
- Privacy policy/notice
- Data collection disclosures
- Use of data descriptions
- Third-party sharing disclosures
- Privacy notice accessibility

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "P2.1",
        "category": "Privacy",
        "title": "Consent",
        "description": "The entity obtains consent for collection and use of personal information.",
        "check_prompt": """Analyze for evidence of consent management.
Look for:
- Consent collection procedures
- Opt-in/opt-out mechanisms
- Consent records
- Consent withdrawal procedures
- Age verification (if applicable)

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "P3.1",
        "category": "Privacy",
        "title": "Data Minimization",
        "description": "The entity limits collection to that necessary for objectives.",
        "check_prompt": """Analyze for evidence of data minimization.
Look for:
- Collection limitation policies
- Purpose specification
- Data necessity assessments
- Retention limitations
- Periodic data reviews

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "P4.1",
        "category": "Privacy",
        "title": "Data Use",
        "description": "The entity limits use of personal information to disclosed purposes.",
        "check_prompt": """Analyze for evidence of data use limitations.
Look for:
- Use limitation policies
- Purpose alignment verification
- Secondary use controls
- Marketing use controls
- Data sharing agreements

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "P5.1",
        "category": "Privacy",
        "title": "Data Subject Rights",
        "description": "The entity grants data subjects access to their personal information.",
        "check_prompt": """Analyze for evidence of data subject rights support.
Look for:
- Access request procedures
- Correction/update procedures
- Deletion procedures
- Data portability
- Response timelines

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "P6.1",
        "category": "Privacy",
        "title": "Data Quality",
        "description": "The entity collects and maintains accurate personal information.",
        "check_prompt": """Analyze for evidence of data quality management.
Look for:
- Data accuracy procedures
- Correction mechanisms
- Data validation
- Regular data reviews
- Quality metrics

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "P7.1",
        "category": "Privacy",
        "title": "Data Security",
        "description": "The entity protects personal information against unauthorized access.",
        "check_prompt": """Analyze for evidence of personal data security.
Look for:
- Encryption of personal data
- Access controls for personal data
- Personal data handling training
- Breach notification procedures
- Security incident procedures

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
    {
        "control_id": "P8.1",
        "category": "Privacy",
        "title": "Third-Party Disclosure",
        "description": "The entity discloses personal information to third parties only with consent.",
        "check_prompt": """Analyze for evidence of third-party disclosure controls.
Look for:
- Third-party data sharing agreements
- Consent for sharing
- Third-party security requirements
- Data processing agreements
- Sub-processor management

Provide JSON response with: status, confidence, summary, evidence_quote, gaps""",
    },
]

# =============================================================================
# COMBINED CONTROLS
# =============================================================================

def get_all_controls() -> list[dict]:
    """Get all SOC 2 controls across all categories."""
    return (
        CC_CONTROLS + 
        AVAILABILITY_CONTROLS + 
        PROCESSING_INTEGRITY_CONTROLS + 
        CONFIDENTIALITY_CONTROLS + 
        PRIVACY_CONTROLS
    )

def get_controls_by_category(category: str) -> list[dict]:
    """Get controls filtered by category."""
    all_controls = get_all_controls()
    return [c for c in all_controls if c["category"].lower() == category.lower()]

def get_control_categories() -> list[dict]:
    """Get list of control categories with counts."""
    categories = {}
    for control in get_all_controls():
        cat = control["category"]
        if cat not in categories:
            categories[cat] = {"name": cat, "count": 0, "controls": []}
        categories[cat]["count"] += 1
        categories[cat]["controls"].append(control["control_id"])
    return list(categories.values())

def get_quick_scan_controls() -> list[dict]:
    """Get subset of controls for quick scan (most critical)."""
    quick_scan_ids = [
        "CC6.1", "CC6.2", "CC6.3",  # Access Controls
        "CC7.2", "CC7.3",           # Security Operations
        "CC8.1",                     # Change Management
        "CC9.1",                     # Risk Management
        "A1.2",                      # Backup & Recovery
    ]
    all_controls = get_all_controls()
    return [c for c in all_controls if c["control_id"] in quick_scan_ids]

def get_control_by_id(control_id: str) -> dict | None:
    """Get a specific control by ID."""
    for control in get_all_controls():
        if control["control_id"] == control_id:
            return control
    return None


# Summary statistics
CONTROL_SUMMARY = {
    "total_controls": len(get_all_controls()),
    "categories": {
        "Common Criteria (Security)": len(CC_CONTROLS),
        "Availability": len(AVAILABILITY_CONTROLS),
        "Processing Integrity": len(PROCESSING_INTEGRITY_CONTROLS),
        "Confidentiality": len(CONFIDENTIALITY_CONTROLS),
        "Privacy": len(PRIVACY_CONTROLS),
    }
}
