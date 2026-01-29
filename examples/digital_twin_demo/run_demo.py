#!/usr/bin/env python3
"""
Digital Twin Integrated Documentation Pipeline — Demo Runner

This script demonstrates the three documentation pipeline modes:
1. Condition-Based Documentation
2. Event-Driven Documentation  
3. Certification Documentation

Usage:
    python run_demo.py --mode all          # Run all three modes
    python run_demo.py --mode condition    # Run condition-based only
    python run_demo.py --mode event        # Run event-driven only
    python run_demo.py --mode certification # Run certification only
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Demo directory
DEMO_DIR = Path(__file__).parent


def print_header(title: str) -> None:
    """Print a formatted header."""
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print()


def print_section(title: str) -> None:
    """Print a section header."""
    print()
    print(f"--- {title} ---")
    print()


def load_yaml_file(path: Path) -> dict:
    """Load a YAML file and return its contents."""
    try:
        import yaml
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except ImportError:
        # Fallback: read as text and show structure
        with open(path, 'r', encoding='utf-8') as f:
            return {"_raw": f.read()[:500] + "..."}


def run_condition_based_demo() -> dict:
    """
    Demonstrate condition-based documentation generation.
    
    Simulates the pipeline that generates maintenance documentation
    when digital twin sensor data indicates conditions requiring attention.
    """
    print_header("CONDITION-BASED DOCUMENTATION PIPELINE")
    
    print("This pipeline generates maintenance documentation when digital twin")
    print("sensors detect conditions requiring attention.")
    print()
    
    # Load health data
    print_section("Loading Digital Twin Health Data")
    health_file = DEMO_DIR / "KDB" / "system_data" / "component_health.yaml"
    health_data = load_yaml_file(health_file)
    
    # Identify triggered conditions
    triggered = []
    if "component_health" in health_data and "components" in health_data["component_health"]:
        for component in health_data["component_health"]["components"]:
            status = component.get("health_status", "unknown")
            if status in ["warning", "caution"]:
                triggered.append({
                    "component_id": component["component_id"],
                    "ata_chapter": component["ata_chapter"],
                    "status": status,
                    "action": component.get("recommended_action", "N/A")
                })
    
    print(f"Components monitored: {len(health_data.get('component_health', {}).get('components', []))}")
    print(f"Conditions triggered: {len(triggered)}")
    print()
    
    if triggered:
        print("Triggered Conditions:")
        for t in triggered:
            print(f"  • {t['component_id']} (ATA {t['ata_chapter']}): {t['status'].upper()}")
            print(f"    Action: {t['action']}")
    
    # Simulate document generation
    print_section("Generating Documentation")
    
    generated_docs = []
    for t in triggered:
        dm_code = f"DMC-DTDEMO-A-{t['ata_chapter']}-00-00-00A-300A-A"
        generated_docs.append({
            "dm_code": dm_code,
            "title": f"Inspection Procedure - {t['component_id']}",
            "type": "procedural",
            "trigger": f"Condition: {t['status']}",
            "source": t["component_id"]
        })
        print(f"  ✓ Generated: {dm_code}")
    
    # Create output
    output_dir = DEMO_DIR / "output" / "condition_based"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report = {
        "pipeline": "condition_based",
        "timestamp": datetime.now().isoformat(),
        "contract_id": "DT-CTR-CONDITION-001",
        "baseline_id": "DBL-DT-DEMO-001",
        "triggered_conditions": triggered,
        "documents_generated": generated_docs,
        "status": "success"
    }
    
    report_file = output_dir / "CONDITION_REPORT.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"\n  ✓ Report saved: {report_file.relative_to(DEMO_DIR)}")
    
    return report


def run_event_driven_demo() -> dict:
    """
    Demonstrate event-driven documentation generation.
    
    Simulates the pipeline that generates troubleshooting documentation
    in response to operational events.
    """
    print_header("EVENT-DRIVEN DOCUMENTATION PIPELINE")
    
    print("This pipeline generates troubleshooting documentation in response")
    print("to operational events captured by digital twin monitoring.")
    print()
    
    # Load event data
    print_section("Loading Operational Events")
    events_file = DEMO_DIR / "KDB" / "events" / "operational_events.yaml"
    events_data = load_yaml_file(events_file)
    
    # Filter events requiring documentation
    actionable_events = []
    if "operational_events" in events_data and "events" in events_data["operational_events"]:
        for event in events_data["operational_events"]["events"]:
            if event.get("requires_documentation", False):
                actionable_events.append({
                    "event_id": event["event_id"],
                    "event_type": event["event_type"],
                    "fault_code": event.get("fault_code") or event.get("warning_code") or event.get("exceedance_code"),
                    "ata_chapter": event["ata_chapter"],
                    "description": event["description"],
                    "priority": event["priority"],
                    "doc_type": event.get("documentation_type", "troubleshooting")
                })
    
    print(f"Total events in log: {len(events_data.get('operational_events', {}).get('events', []))}")
    print(f"Events requiring documentation: {len(actionable_events)}")
    print()
    
    if actionable_events:
        print("Events to Process:")
        for e in actionable_events:
            print(f"  • [{e['priority'].upper()}] {e['fault_code']}: {e['description'][:50]}...")
    
    # Simulate document generation
    print_section("Generating Documentation")
    
    generated_docs = []
    for e in actionable_events:
        info_code = "700" if e["doc_type"] == "fault_isolation" else "710"
        dm_code = f"DMC-DTDEMO-A-{e['ata_chapter']}-00-00-00A-{info_code}A-A"
        generated_docs.append({
            "dm_code": dm_code,
            "title": f"{e['doc_type'].replace('_', ' ').title()} - {e['fault_code']}",
            "type": e["doc_type"],
            "trigger": f"Event: {e['event_id']}",
            "source": e["fault_code"]
        })
        print(f"  ✓ Generated: {dm_code}")
    
    # Create output
    output_dir = DEMO_DIR / "output" / "event_driven"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report = {
        "pipeline": "event_driven",
        "timestamp": datetime.now().isoformat(),
        "contract_id": "DT-CTR-EVENT-001",
        "baseline_id": "DBL-DT-DEMO-001",
        "events_processed": actionable_events,
        "documents_generated": generated_docs,
        "status": "success"
    }
    
    report_file = output_dir / "EVENT_RESPONSE_REPORT.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"\n  ✓ Report saved: {report_file.relative_to(DEMO_DIR)}")
    
    return report


def run_certification_demo() -> dict:
    """
    Demonstrate certification documentation generation.
    
    Simulates the pipeline that generates evidence packages
    for regulatory compliance.
    """
    print_header("CERTIFICATION DOCUMENTATION PIPELINE")
    
    print("This pipeline generates certification evidence packages for")
    print("regulatory compliance and continued airworthiness.")
    print()
    
    # Load requirements and contract
    print_section("Loading Certification Context")
    contract_file = DEMO_DIR / "ASIT" / "CONTRACTS" / "active" / "DT-CTR-CERT-001.yaml"
    load_yaml_file(contract_file)
    
    req_file = DEMO_DIR / "KDB" / "requirements" / "digital_twin_requirements.yaml"
    req_data = load_yaml_file(req_file)
    
    # Extract certification requirements
    cert_requirements = []
    if "requirements" in req_data and "items" in req_data["requirements"]:
        for req in req_data["requirements"]["items"]:
            if req.get("certification_relevant", False):
                cert_requirements.append({
                    "requirement_id": req["requirement_id"],
                    "title": req["title"],
                    "ata_chapter": req["ata_chapter"],
                    "verification": req.get("verification_method", "analysis"),
                    "traces_to": req.get("traces_to", [])
                })
    
    print(f"Certification-relevant requirements: {len(cert_requirements)}")
    print()
    
    if cert_requirements:
        print("Requirements for Compliance Matrix:")
        for r in cert_requirements[:5]:  # Show first 5
            regs = ", ".join(r["traces_to"][:2]) if r["traces_to"] else "N/A"
            print(f"  • {r['requirement_id']}: {r['title'][:40]}...")
            print(f"    Regulatory: {regs}")
    
    # Build compliance matrix
    print_section("Building Compliance Matrix")
    
    compliance_items = []
    for r in cert_requirements:
        compliance_items.append({
            "requirement_id": r["requirement_id"],
            "regulatory_reference": r["traces_to"][0] if r["traces_to"] else "N/A",
            "status": "compliant",
            "verification_method": r["verification"],
            "evidence_reference": f"EVD-{r['requirement_id']}"
        })
        print(f"  ✓ {r['requirement_id']} → compliant ({r['verification']})")
    
    # Generate certification documents
    print_section("Generating Certification Documents")
    
    generated_docs = [
        {
            "document_type": "compliance_matrix",
            "filename": "COMPLIANCE_MATRIX.xml",
            "items": len(compliance_items)
        },
        {
            "document_type": "evidence_package",
            "filename": "EVIDENCE_PACKAGE.xml",
            "items": len(compliance_items)
        },
        {
            "document_type": "traceability_report",
            "filename": "TRACEABILITY_REPORT.xml",
            "items": len(compliance_items)
        },
        {
            "document_type": "certification_summary",
            "filename": "CERTIFICATION_SUMMARY.xml",
            "items": 1
        }
    ]
    
    for doc in generated_docs:
        print(f"  ✓ Generated: {doc['filename']} ({doc['items']} items)")
    
    # Create output
    output_dir = DEMO_DIR / "output" / "certification"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create compliance matrix
    compliance_matrix = {
        "metadata": {
            "directive": "AD-2026-01-15-DEMO",
            "subject": "Fuel System Inspection Requirements",
            "generated": datetime.now().isoformat(),
            "contract_id": "DT-CTR-CERT-001",
            "baseline_id": "DBL-DT-DEMO-001"
        },
        "compliance_items": compliance_items,
        "summary": {
            "total_items": len(compliance_items),
            "compliant": len(compliance_items),
            "partially_compliant": 0,
            "non_compliant": 0,
            "pending": 0
        }
    }
    
    matrix_file = output_dir / "COMPLIANCE_MATRIX.json"
    with open(matrix_file, 'w', encoding='utf-8') as f:
        json.dump(compliance_matrix, f, indent=2)
    print(f"\n  ✓ Compliance matrix saved: {matrix_file.relative_to(DEMO_DIR)}")
    
    # Create certification report
    report = {
        "pipeline": "certification",
        "timestamp": datetime.now().isoformat(),
        "contract_id": "DT-CTR-CERT-001",
        "baseline_id": "DBL-DT-DEMO-001",
        "regulatory_reference": "AD-2026-01-15-DEMO",
        "requirements_evaluated": len(cert_requirements),
        "compliance_summary": compliance_matrix["summary"],
        "documents_generated": generated_docs,
        "package_hash": "sha256:demo_hash_placeholder",
        "status": "success"
    }
    
    report_file = output_dir / "CERTIFICATION_STATUS_REPORT.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"  ✓ Status report saved: {report_file.relative_to(DEMO_DIR)}")
    
    return report


def run_demo(mode: str) -> int:
    """Run the demo in the specified mode."""
    
    print_header("DIGITAL TWIN INTEGRATED DOCUMENTATION PIPELINE")
    print("                     DEMONSTRATION")
    
    print(f"Demo Directory: {DEMO_DIR}")
    print(f"Mode: {mode}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    results = {}
    
    try:
        if mode in ("all", "condition"):
            results["condition"] = run_condition_based_demo()
            
        if mode in ("all", "event"):
            results["event"] = run_event_driven_demo()
            
        if mode in ("all", "certification"):
            results["certification"] = run_certification_demo()
            
        # Summary
        print_header("DEMO COMPLETE")
        
        print("Pipeline Results:")
        for pipeline, result in results.items():
            status = result.get("status", "unknown")
            docs = len(result.get("documents_generated", []))
            print(f"  • {pipeline.upper()}: {status} ({docs} documents generated)")
        
        print()
        print("Output Locations:")
        print(f"  • Condition-based: output/condition_based/")
        print(f"  • Event-driven:    output/event_driven/")
        print(f"  • Certification:   output/certification/")
        print()
        print("Review the generated JSON reports for detailed results.")
        print()
        
        return 0
        
    except Exception as e:
        print()
        print(f"ERROR: {e}")
        print()
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Digital Twin Documentation Pipeline Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_demo.py --mode all           # Run all pipeline modes
  python run_demo.py --mode condition     # Condition-based only
  python run_demo.py --mode event         # Event-driven only
  python run_demo.py --mode certification # Certification only
        """
    )
    
    parser.add_argument(
        "--mode", "-m",
        choices=["all", "condition", "event", "certification"],
        default="all",
        help="Pipeline mode to demonstrate (default: all)"
    )
    
    args = parser.parse_args()
    
    return run_demo(args.mode)


if __name__ == "__main__":
    sys.exit(main())
