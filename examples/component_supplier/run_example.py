#!/usr/bin/env python3
"""
Component Supplier Example — Run Script

Demonstrates AEROSPACEMODEL for Tier-1 aerospace suppliers.
"""

import argparse
import sys
from pathlib import Path

example_dir = Path(__file__).parent
repo_root = example_dir.parent.parent
sys.path.insert(0, str(repo_root / "src"))


def main():
    parser = argparse.ArgumentParser(description="Run Component Supplier example")
    parser.add_argument("--contract", help="Specific contract to run")
    parser.add_argument("--all", action="store_true", help="Run all contracts")
    parser.add_argument("--baseline", default="CBL-LGA5000-2026-Q1", help="Baseline ID")
    parser.add_argument("--customer", help="Filter by customer (OEM-A, OEM-B)")
    args = parser.parse_args()
    
    print("=" * 70)
    print("AEROSPACEMODEL — Component Supplier Example")
    print("Supplier: AeroParts International (API01)")
    print("Product: LGA-5000 Landing Gear Actuator")
    print("=" * 70)
    print()
    
    contracts = {
        "API-CTR-CMM-001": {
            "name": "Component Maintenance Manual",
            "baseline": "CBL-LGA5000-2026-Q1",
            "scope": "LGA-5000 Series Maintenance/Overhaul"
        },
        "API-CTR-IPC-001": {
            "name": "Illustrated Parts Catalog",
            "baseline": "CBL-LGA5000-2026-Q1",
            "scope": "LGA-5000 Series Parts Breakdown"
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
        print("  python run_example.py --contract API-CTR-CMM-001")
        print("  python run_example.py --all")
        print("  python run_example.py --contract API-CTR-CMM-001 --customer OEM-A")
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
        if args.customer:
            print(f"Customer Filter: {args.customer}")
        print("-" * 70)
        
        run_transformation(contract_id, baseline, info, args.customer)
        print()
    
    print("=" * 70)
    print("Complete!")
    print("=" * 70)
    return 0


def run_transformation(contract_id, baseline_id, info, customer_filter=None):
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
            baseline=baseline,
            customer_filter=customer_filter
        )
        
        result = engine.execute()
        print(f"✓ Generated {result.dm_count} Data Module(s)")
        
    except ImportError:
        print("Note: Running in demo mode (AEROSPACEMODEL not installed)")
        demo_transformation(contract_id, info, customer_filter)


def demo_transformation(contract_id, info, customer_filter=None):
    """Simulate transformation for demo purposes."""
    
    import json
    from datetime import datetime
    
    run_id = datetime.now().strftime("%Y%m%d-%H%M") + f"__{contract_id}"
    runs_dir = example_dir / "ASIGT" / "runs" / run_id
    runs_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine output type and counts
    if "IPC" in contract_id:
        pub_type = "ipc"
        dm_count = 8
    else:
        pub_type = "cmm"
        dm_count = 15
    
    if customer_filter:
        dm_count = dm_count // 2  # Reduced for single customer
    
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
        "supplier_type": "Tier-1",
        "duration_seconds": 2.8,
        "dms_generated": dm_count,
        "validation_pass_rate": 1.0,
        "customer_filter": customer_filter,
        "as9100_compliant": True
    }
    (runs_dir / "METRICS.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    print(f"✓ Reports saved to ASIGT/runs/{run_id}/")


if __name__ == "__main__":
    sys.exit(main())
