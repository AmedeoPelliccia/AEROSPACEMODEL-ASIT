#!/usr/bin/env python3
"""
Regional Jet Example — Run Script

Demonstrates running multiple AEROSPACEMODEL transformations for a full program.
"""

import argparse
import sys
from pathlib import Path

example_dir = Path(__file__).parent
repo_root = example_dir.parent.parent
sys.path.insert(0, str(repo_root / "src"))


def main():
    parser = argparse.ArgumentParser(description="Run Regional Jet example")
    parser.add_argument("--contract", help="Specific contract to run")
    parser.add_argument("--all", action="store_true", help="Run all contracts")
    parser.add_argument("--baseline", default="FBL-RJ7-2026-Q1", help="Baseline ID")
    args = parser.parse_args()
    
    print("=" * 70)
    print("AEROSPACEMODEL — Regional Jet Example")
    print("Program: RegionalJet-700 (RJ7)")
    print("=" * 70)
    print()
    
    contracts = {
        "RJ7-CTR-AMM-001": {
            "name": "Aircraft Maintenance Manual",
            "baseline": "FBL-RJ7-2026-Q1",
            "scope": "ATA 21, 24, 27, 28, 29, 32, 72"
        },
        "RJ7-CTR-IPC-001": {
            "name": "Illustrated Parts Catalog",
            "baseline": "PBL-RJ7-2026-Q1",
            "scope": "All chapters"
        },
        "RJ7-CTR-SRM-001": {
            "name": "Structural Repair Manual",
            "baseline": "FBL-RJ7-2026-Q1",
            "scope": "ATA 52, 53, 57"
        }
    }
    
    if args.contract:
        to_run = [args.contract]
    elif args.all:
        to_run = list(contracts.keys())
    else:
        print("Available contracts:")
        for cid, info in contracts.items():
            print(f"  • {cid}: {info['name']} ({info['scope']})")
        print()
        print("Usage:")
        print("  python run_example.py --contract RJ7-CTR-AMM-001")
        print("  python run_example.py --all")
        return 0
    
    for contract_id in to_run:
        if contract_id not in contracts:
            print(f"Unknown contract: {contract_id}")
            continue
            
        info = contracts[contract_id]
        baseline = args.baseline if args.contract else info["baseline"]
        
        print("-" * 70)
        print(f"Contract: {contract_id}")
        print(f"Publication: {info['name']}")
        print(f"Baseline: {baseline}")
        print(f"Scope: {info['scope']}")
        print("-" * 70)
        
        run_transformation(contract_id, baseline, info)
        print()
    
    print("=" * 70)
    print("Complete!")
    print("=" * 70)
    return 0


def run_transformation(contract_id, baseline_id, info):
    """Execute a single transformation contract."""
    
    try:
        from aerospacemodel.asigt.engine import TransformationEngine
        from aerospacemodel.asit.contracts import ContractLoader
        from aerospacemodel.asit.baselines import BaselineManager
        
        contract_loader = ContractLoader(example_dir / "ASIT" / "CONTRACTS")
        contract = contract_loader.load(contract_id)
        
        baseline_mgr = BaselineManager(example_dir / "ASIT" / "GOVERNANCE")
        baseline = baseline_mgr.get(baseline_id)
        
        engine = TransformationEngine(
            config_path=example_dir / "program_config.yaml",
            contract=contract,
            baseline=baseline
        )
        
        result = engine.execute()
        print(f"✓ Generated {result.dm_count} Data Module(s)")
        
        engine.generate_reports()
        print(f"✓ Reports saved to ASIGT/runs/{result.run_id}/")
        
    except ImportError:
        print("Note: Running in demo mode (AEROSPACEMODEL not installed)")
        demo_transformation(contract_id, info)


def demo_transformation(contract_id, info):
    """Simulate transformation for demo purposes."""
    
    import json
    from datetime import datetime
    
    run_id = datetime.now().strftime("%Y%m%d-%H%M") + f"__{contract_id}"
    runs_dir = example_dir / "ASIGT" / "runs" / run_id
    runs_dir.mkdir(parents=True, exist_ok=True)
    
    pub_type = contract_id.split("-")[2].lower()
    output_dir = example_dir / "output" / pub_type
    output_dir.mkdir(parents=True, exist_ok=True)
    
    idb_dir = example_dir / "IDB" / "csdb" / "dms"
    idb_dir.mkdir(parents=True, exist_ok=True)
    
    # Simulate DM generation count
    dm_counts = {"AMM": 15, "IPC": 8, "SRM": 6}
    pub = contract_id.split("-")[2]
    count = dm_counts.get(pub, 5)
    
    print(f"✓ Generated {count} Data Module(s) (demo mode)")
    
    # Create metrics
    metrics = {
        "run_id": run_id,
        "contract_id": contract_id,
        "publication": info["name"],
        "duration_seconds": 2.5,
        "dms_generated": count,
        "validation_pass_rate": 1.0
    }
    (runs_dir / "METRICS.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    print(f"✓ Reports saved to ASIGT/runs/{run_id}/")


if __name__ == "__main__":
    sys.exit(main())
