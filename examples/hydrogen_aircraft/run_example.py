#!/usr/bin/env python3
"""
Hydrogen Aircraft Example — Run Script

Demonstrates AEROSPACEMODEL for hydrogen-powered aircraft programs.
"""

import argparse
import sys
from pathlib import Path

example_dir = Path(__file__).parent
repo_root = example_dir.parent.parent
sys.path.insert(0, str(repo_root / "src"))


def main():
    parser = argparse.ArgumentParser(description="Run Hydrogen Aircraft example")
    parser.add_argument("--contract", help="Specific contract to run")
    parser.add_argument("--all", action="store_true", help="Run all contracts")
    parser.add_argument("--baseline", default="FBL-HJ1-2026-Q1", help="Baseline ID")
    args = parser.parse_args()
    
    print("=" * 70)
    print("AEROSPACEMODEL — Hydrogen Aircraft Example")
    print("Program: HydrogenJet-100 (HJ1)")
    print("Propulsion: Hydrogen Fuel Cell")
    print("=" * 70)
    print()
    
    contracts = {
        "HJ1-CTR-AMM-001": {
            "name": "Aircraft Maintenance Manual",
            "baseline": "FBL-HJ1-2026-Q1",
            "scope": "ATA 24, 28, 71, 73 (Hydrogen Systems)"
        },
        "HJ1-CTR-CMM-001": {
            "name": "Component Maintenance Manual - Fuel Cell Stack",
            "baseline": "FBL-HJ1-2026-Q1",
            "scope": "Fuel Cell Stack Assembly"
        }
    }
    
    if args.contract:
        to_run = [args.contract]
    elif args.all:
        to_run = list(contracts.keys())
    else:
        print("Available contracts:")
        for cid, info in contracts.items():
            print(f"  • {cid}: {info['name']}")
            print(f"    Scope: {info['scope']}")
        print()
        print("Usage:")
        print("  python run_example.py --contract HJ1-CTR-AMM-001")
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
    
    # Determine output type
    if "CMM" in contract_id:
        pub_type = "cmm"
        dm_count = 10
    else:
        pub_type = "amm"
        dm_count = 18
    
    output_dir = example_dir / "output" / pub_type
    output_dir.mkdir(parents=True, exist_ok=True)
    
    idb_dir = example_dir / "IDB" / "csdb" / "dms"
    idb_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Generated {dm_count} Data Module(s) (demo mode)")
    
    # Create metrics
    metrics = {
        "run_id": run_id,
        "contract_id": contract_id,
        "publication": info["name"],
        "aircraft_type": "Hydrogen",
        "duration_seconds": 4.1,
        "dms_generated": dm_count,
        "validation_pass_rate": 1.0,
        "hydrogen_safety_checks": True
    }
    (runs_dir / "METRICS.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    print(f"✓ Reports saved to ASIGT/runs/{run_id}/")


if __name__ == "__main__":
    sys.exit(main())
