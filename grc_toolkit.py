
#!/usr/bin/env python3
"""
GRC Data Analysis Toolkit - Week 1
Part 1: Organizational Profile Analyzer
Part 2: CIA Triad Impact Classifier
"""

from dataclasses import dataclass
from datetime import datetime


# ============================================================
# PART 1: ORGANIZATIONAL PROFILE ANALYZER
# ============================================================

def identify_applicable_regulations(org_profile: dict) -> list:
    """Identify potentially applicable frameworks for an organization."""
    regulations = []
    sector = org_profile.get("sector", "").lower()
    employees = org_profile.get("employees", 0)

    if org_profile.get("handles_health_data", False) or sector in (
        "healthcare", "hospital", "clinic"
    ):
        regulations.append({
            "name": "HIPAA Security Rule",
            "reason": "Organization handles protected health information",
            "priority": "MANDATORY",
            "key_requirement": "Risk analysis and security safeguards",
        })

    if org_profile.get("processes_payments", False):
        regulations.append({
            "name": "PCI DSS v4.0",
            "reason": "Organization processes payment card data",
            "priority": "MANDATORY",
            "key_requirement": "Payment card data security controls",
        })

    if org_profile.get("handles_eu_personal_data", False):
        regulations.append({
            "name": "GDPR",
            "reason": "Organization processes EU residents' personal data",
            "priority": "MANDATORY",
            "key_requirement": "Lawful processing and data subject rights",
        })

    if sector in (
        "banking", "financial services", "insurance", "fintech"
    ):
        regulations.append({
            "name": "GLBA Safeguards Rule",
            "reason": "Potential financial institution requirements",
            "priority": "MANDATORY",
            "key_requirement": "Written information security program",
        })

    if org_profile.get("public_company", False):
        regulations.append({
            "name": "SOX IT Controls (Section 404)",
            "reason": "Public company financial reporting controls",
            "priority": "MANDATORY",
            "key_requirement": "Internal control over financial reporting",
        })

    if (
        org_profile.get("is_federal_contractor", False)
        or sector == "government"
    ):
        regulations.append({
            "name": "FISMA / NIST SP 800-53",
            "reason": "Potential federal security requirements",
            "priority": "MANDATORY",
            "key_requirement": "Security controls and continuous monitoring",
        })

    if org_profile.get("handles_cui", False) or sector == "defense":
        regulations.append({
            "name": "CMMC 2.0",
            "reason": "Potential DoD contractor security requirements",
            "priority": "MANDATORY",
            "key_requirement": "Required CMMC level depends on contract",
        })

    if org_profile.get("california_presence", False) and employees >= 1:
        regulations.append({
            "name": "CCPA/CPRA",
            "reason": "California privacy applicability needs verification",
            "priority": "LIKELY APPLICABLE - verify thresholds",
            "key_requirement": "Consumer privacy rights and disclosures",
        })

    regulations.append({
        "name": "NIST Cybersecurity Framework 2.0",
        "reason": "Recommended cybersecurity risk management framework",
        "priority": "STRONGLY RECOMMENDED",
        "key_requirement": "Govern, Identify, Protect, Detect, Respond, Recover",
    })

    return regulations


def assess_governance_maturity(org_profile: dict) -> dict:
    """Score governance, risk, and compliance maturity from 1 to 5."""
    scores = {"governance": 1.0, "risk": 1.0, "compliance": 1.0}
    evidence = {"governance": [], "risk": [], "compliance": []}

    governance_checks = {
        "has_ciso": "CISO or dedicated security leader exists",
        "has_security_committee": "Security committee established",
        "board_security_reporting": "Board receives security reports",
        "security_budget_defined": "Security budget is defined",
        "policy_suite_current": "Security policies are current",
    }

    for field, description in governance_checks.items():
        if org_profile.get(field, False):
            scores["governance"] += (
                0.5 if field in (
                    "security_budget_defined", "policy_suite_current"
                ) else 1
            )
            evidence["governance"].append(description)

    risk_checks = {
        "has_risk_register": "Formal risk register maintained",
        "annual_risk_assessment": "Annual risk assessment conducted",
        "continuous_risk_monitoring": "Continuous risk monitoring in place",
        "risk_appetite_documented": "Risk appetite is documented",
    }

    for field, description in risk_checks.items():
        if org_profile.get(field, False):
            scores["risk"] += 1
            evidence["risk"].append(description)

    compliance_checks = {
        "compliance_program": "Formal compliance program exists",
        "last_audit_passed": "Most recent audit passed",
        "security_training": "Security awareness training is active",
        "vendor_risk_program": "Third-party risk program exists",
    }

    for field, description in compliance_checks.items():
        if org_profile.get(field, False):
            scores["compliance"] += 1
            evidence["compliance"].append(description)

    for dimension in scores:
        scores[dimension] = min(5.0, round(scores[dimension], 1))

    return {
        "scores": scores,
        "evidence": evidence,
        "overall_maturity": round(sum(scores.values()) / 3, 1),
    }


def generate_grc_summary_report(org_profile: dict) -> str:
    """Generate a readable report of regulations and maturity scores."""
    regulations = identify_applicable_regulations(org_profile)
    maturity = assess_governance_maturity(org_profile)

    lines = [
        "=" * 65,
        "GRC READINESS ASSESSMENT REPORT",
        f"Organization: {org_profile.get('org_name', 'Unknown')}",
        f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
        "=" * 65,
        "",
        "APPLICABLE REGULATORY FRAMEWORKS",
        "-" * 65,
    ]

    mandatory = [r for r in regulations if r["priority"] == "MANDATORY"]
    recommended = [r for r in regulations if r["priority"] != "MANDATORY"]

    lines.append(f"MANDATORY ({len(mandatory)} frameworks):")
    for regulation in mandatory:
        lines.append(f"  [REVIEW] {regulation['name']}")
        lines.append(f"  Reason: {regulation['reason']}")
        lines.append(f"  Key requirement: {regulation['key_requirement']}")
        lines.append("")

    lines.append(f"RECOMMENDED / VERIFY ({len(recommended)} frameworks):")
    for regulation in recommended:
        lines.append(f"  {regulation['name']} - {regulation['priority']}")
        lines.append(f"  Reason: {regulation['reason']}")
        lines.append("")

    lines.extend([
        "GRC MATURITY SCORES (1 = Initial, 5 = Optimizing)",
        "-" * 65,
    ])

    labels = {
        1: "Initial/Ad-hoc",
        2: "Developing",
        3: "Defined",
        4: "Managed",
        5: "Optimizing",
    }

    for dimension, score in maturity["scores"].items():
        lines.append(
            f"{dimension.upper():<12} {score}/5 "
            f"({labels.get(round(score), 'Intermediate')})"
        )
        for item in maturity["evidence"][dimension]:
            lines.append(f"  + {item}")

    overall = maturity["overall_maturity"]
    if overall < 2:
        status = "CRITICAL GAPS - immediate improvement needed"
    elif overall < 3:
        status = "DEVELOPING - significant improvement needed"
    elif overall < 4:
        status = "DEFINED - improve consistency"
    else:
        status = "MANAGED - focus on optimization"

    lines.extend([
        "",
        f"OVERALL GRC MATURITY: {overall}/5",
        status,
        "",
        "Note: This is an educational screening tool, not legal advice.",
        "Verify actual applicability with qualified compliance professionals.",
        "=" * 65,
    ])

    return "\n".join(lines)


# ============================================================
# PART 2: CIA TRIAD IMPACT CLASSIFIER
# ============================================================

@dataclass
class SecurityEvent:
    """Represent a security incident with a name and description."""
    name: str
    description: str


def classify_cia_impact(event: SecurityEvent) -> dict:
    """Classify confidentiality, integrity, availability, and severity."""
    text = f"{event.name} {event.description}".lower()

    confidentiality_keywords = [
        "data exposed", "leaked", "unauthorized access", "breach",
        "exfiltrat", "credential", "eavesdrop", "intercept",
        "disclosed", "stolen", "read by unauthorized",
        "viewed by unauthorized",
    ]

    integrity_keywords = [
        "modified", "tampered", "altered", "corrupted", "falsif",
        "changed without", "forged", "injected", "replaced",
        "sql inject", "man-in-the-middle",
    ]

    availability_keywords = [
        "unavailable", "down", "outage", "ransomware", "encrypt",
        "ddos", "denial of service", "locked out", "deleted",
        "wiped", "destroyed", "inaccessible",
    ]

    confidentiality = any(k in text for k in confidentiality_keywords)
    integrity = any(k in text for k in integrity_keywords)
    availability = any(k in text for k in availability_keywords)

    # Select the primary impact using a consistent precedence.
    if availability:
        primary = "AVAILABILITY"
    elif confidentiality:
        primary = "CONFIDENTIALITY"
    elif integrity:
        primary = "INTEGRITY"
    else:
        primary = "UNCLEAR"

    affected_count = sum([confidentiality, integrity, availability])
    severity = min(3, affected_count) if affected_count else 1
    severity_labels = {1: "LOW", 2: "MEDIUM", 3: "HIGH"}

    return {
        "event": event.name,
        "confidentiality_affected": confidentiality,
        "integrity_affected": integrity,
        "availability_affected": availability,
        "primary_impact": primary,
        "severity": severity,
        "severity_label": severity_labels[severity],
    }


def print_cia_report(events: list[SecurityEvent]) -> None:
    """Print a formatted CIA triad classification report."""
    print("\n" + "=" * 90)
    print("CIA TRIAD IMPACT CLASSIFICATION REPORT")
    print("=" * 90)

    print(
        f"{'EVENT':<29} {'C':^3} {'I':^3} {'A':^3} "
        f"{'PRIMARY':<18} {'SEV':^6}"
    )
    print("-" * 90)

    for event in events:
        result = classify_cia_impact(event)
        c = "✓" if result["confidentiality_affected"] else "✗"
        i = "✓" if result["integrity_affected"] else "✗"
        a = "✓" if result["availability_affected"] else "✗"

        print(
            f"{event.name[:28]:<29} {c:^3} {i:^3} {a:^3} "
            f"{result['primary_impact']:<18} "
            f"{result['severity_label']:^6}"
        )

    print("=" * 90)
    print("C = Confidentiality | I = Integrity | A = Availability")


# ============================================================
# MAIN: DEMONSTRATION AND TEST CASES
# ============================================================

if __name__ == "__main__":
    # Replace this example with your actual Lab 1 case company.
    company = {
        "org_name": "HealthBridge Medical Center",
        "sector": "healthcare",
        "employees": 2800,
        "handles_health_data": True,
        "processes_payments": True,
        "handles_eu_personal_data": False,
        "public_company": False,
        "is_federal_contractor": False,
        "handles_cui": False,
        "california_presence": False,
        "has_ciso": False,
        "has_security_committee": False,
        "board_security_reporting": False,
        "security_budget_defined": False,
        "policy_suite_current": False,
        "has_risk_register": False,
        "annual_risk_assessment": True,
        "continuous_risk_monitoring": False,
        "risk_appetite_documented": False,
        "compliance_program": True,
        "last_audit_passed": True,
        "security_training": False,
        "vendor_risk_program": False,
    }

    print(generate_grc_summary_report(company))

    test_events = [
        SecurityEvent(
            "HealthBridge PHI Breach",
            "Stolen credential; 14,200 patient records exposed "
            "to an unauthorized party",
        ),
        SecurityEvent(
            "Hospital Ransomware Attack",
            "Systems encrypted by ransomware; EHR unavailable for 5 days",
        ),
        SecurityEvent(
            "EHR Record Tampering",
            "Medication dosage records altered in the EHR",
        ),
        SecurityEvent(
            "DDoS on Bank Portal",
            "Online banking portal unavailable for 6 hours via DDoS",
        ),
        SecurityEvent(
            "SQL Injection Attack",
            "Attacker injected SQL into a web form; records altered",
        ),
        SecurityEvent(
            "Laptop Theft",
            "Unencrypted laptop containing employee SSNs was stolen",
        ),
        SecurityEvent(
            "Insider Data Exfiltration",
            "Employee emailed customer records to a personal email",
        ),
        SecurityEvent(
            "Power Outage",
            "Data center outage; servers unavailable for 3 hours",
        ),
    ]

    print_cia_report(test_events)

    print("\nRun this toolkit with your own Lab 1 company profile.")