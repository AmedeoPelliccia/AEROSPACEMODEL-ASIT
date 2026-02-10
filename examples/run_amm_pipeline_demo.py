#!/usr/bin/env python3
"""
S1000D AMM Content Pipeline Example

This example demonstrates the complete S1000D AMM content pipeline
execution from source data to deliverable technical publications.

The pipeline implements five stages:
1. INGEST & NORMALIZE - Load and normalize source data
2. VALIDATE & ENRICH - Apply business rules and enrich content
3. TRANSFORM TO S1000D - Transform to S1000D data modules
4. ASSEMBLE DATA MODULES - Assemble into publication structure
5. PUBLISH & QA - Render outputs and perform quality assurance

Usage:
    python examples/run_amm_pipeline_demo.py
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import yaml

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aerospacemodel.asigt.pipeline import execute_pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


def print_banner():
    """Print pipeline banner."""
    banner = """
┌─────────────────────────────────────────────────────────────────────────┐
│                    S1000D AMM CONTENT PIPELINE                         │
│                                                                        │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────┐│
│  │ INGEST & │──▶│ VALIDATE │──▶│TRANSFORM │──▶│ ASSEMBLE │──▶│PUBLISH││
│  │ NORMALIZE│   │ & ENRICH │   │ TO S1000D│   │ DATA     │   │& QA  ││
│  └──────────┘   └──────────┘   └──────────┘   │ MODULES  │   └──────┘│
│                                                └──────────┘           │
│                                                                        │
│  Sources:        Rules:         XSLT/Code:     CSDB:        Output:   │
│  - OEM Data      - BREX         - DM Mapping   - DM Assembly - IETP   │
│  - Engineering   - Bus. Rules   - SNS Coding   - PM/IPD Gen  - PDF    │
│  - Legacy Docs   - Schema Val   - ICN Handling - Applicab.   - IETM   │
└─────────────────────────────────────────────────────────────────────────┘
    """
    print(banner)


def setup_demo_environment(base_path: Path) -> tuple[Path, Path, Path]:
    """
    Setup demo environment with sample data.
    
    Args:
        base_path: Base directory for demo
        
    Returns:
        Tuple of (kdb_root, output_path, pipeline_config_path)
    """
    logger.info("Setting up demo environment...")
    
    # Create directory structure
    kdb_root = base_path / "demo_kdb"
    output_path = base_path / "demo_output"
    config_path = base_path / "demo_config"
    
    for path in [kdb_root, output_path, config_path]:
        path.mkdir(parents=True, exist_ok=True)
    
    # Create KDB structure
    (kdb_root / "SSOT" / "requirements").mkdir(parents=True, exist_ok=True)
    (kdb_root / "SSOT" / "tasks").mkdir(parents=True, exist_ok=True)
    (kdb_root / "SSOT" / "graphics").mkdir(parents=True, exist_ok=True)
    
    # Create sample requirements
    requirements = [
        {
            "id": "REQ-ATA28-001",
            "ata_chapter": "28",
            "title": "Fuel System Description",
            "description": "The fuel system shall provide fuel to all engines during all flight phases.",
            "type": "functional",
            "safety_critical": True
        },
        {
            "id": "REQ-ATA28-002",
            "ata_chapter": "28",
            "title": "Fuel Quantity Indication",
            "description": "The fuel quantity indication system shall display fuel quantity with ±1% accuracy.",
            "type": "performance",
            "safety_critical": False
        },
        {
            "id": "REQ-ATA27-001",
            "ata_chapter": "27",
            "title": "Flight Control System",
            "description": "The flight control system shall provide aircraft control in all normal and abnormal conditions.",
            "type": "functional",
            "safety_critical": True
        }
    ]
    
    for req in requirements:
        req_file = kdb_root / "SSOT" / "requirements" / f"{req['id']}.yaml"
        with open(req_file, "w", encoding="utf-8") as f:
            yaml.dump(req, f)
    
    logger.info(f"Created {len(requirements)} sample requirements")
    
    # Create sample tasks
    tasks = [
        {
            "id": "TASK-ATA28-001",
            "ata_chapter": "28",
            "title": "Fuel Tank Inspection",
            "description": "Inspect fuel tank for contamination and damage",
            "task_type": "inspection",
            "steps": [
                "Drain fuel from tank",
                "Inspect tank interior for corrosion",
                "Check for water contamination",
                "Clean and dry tank"
            ],
            "warnings": [
                "Ensure adequate ventilation",
                "No open flames"
            ],
            "tools": ["Flashlight", "Inspection mirror"],
            "estimated_time_hours": 2.0
        },
        {
            "id": "TASK-ATA28-002",
            "ata_chapter": "28",
            "title": "Fuel Pump Replacement",
            "description": "Remove and replace fuel boost pump",
            "task_type": "removal",
            "steps": [
                "Isolate fuel pump circuit breaker",
                "Drain fuel from tank",
                "Disconnect electrical connectors",
                "Remove fuel pump mounting bolts",
                "Remove fuel pump"
            ],
            "warnings": [
                "Fuel is flammable",
                "Disconnect power before working"
            ],
            "tools": ["Wrench set", "Torque wrench"],
            "estimated_time_hours": 4.0
        }
    ]
    
    for task in tasks:
        task_file = kdb_root / "SSOT" / "tasks" / f"{task['id']}.yaml"
        with open(task_file, "w", encoding="utf-8") as f:
            yaml.dump(task, f)
    
    logger.info(f"Created {len(tasks)} sample tasks")
    
    # Create pipeline configuration
    pipeline_config = {
        "pipeline": {
            "metadata": {
                "pipeline_id": "DEMO-AMM-001",
                "name": "Demo AMM Content Pipeline",
                "description": "Demonstration pipeline for S1000D AMM content generation",
                "version": "1.0.0",
                "publication_type": "AMM",
                "owner": "Demo Team",
                "tags": ["demo", "amm", "s1000d"]
            },
            "contract": {
                "template": "ASIT/CONTRACTS/templates/KITDM-CTR-LM-CSDB.template.yaml",
                "required_fields": [
                    "contract_id",
                    "baseline_ref"
                ]
            },
            "stages": [
                {
                    "stage": "initialization",
                    "name": "Pipeline Initialization",
                    "description": "Initialize pipeline and validate prerequisites",
                    "order": 1
                },
                {
                    "stage": "source_loading",
                    "name": "Source Loading",
                    "description": "Load source artifacts from KDB baseline",
                    "order": 2
                },
                {
                    "stage": "transformation",
                    "name": "Content Transformation",
                    "description": "Transform sources to S1000D data modules",
                    "order": 3
                },
                {
                    "stage": "validation",
                    "name": "Content Validation",
                    "description": "Validate against BREX and schema",
                    "order": 4
                },
                {
                    "stage": "publication_assembly",
                    "name": "Publication Assembly",
                    "description": "Assemble data modules into publication",
                    "order": 5
                },
                {
                    "stage": "rendering",
                    "name": "Output Rendering",
                    "description": "Render to deliverable formats",
                    "order": 6
                },
                {
                    "stage": "finalization",
                    "name": "Pipeline Finalization",
                    "description": "Finalize and archive artifacts",
                    "order": 7
                }
            ],
            "config": {
                "execution": {
                    "parallel_enabled": True,
                    "max_parallel_steps": 4,
                    "timeout_minutes": 60
                },
                "logging": {
                    "level": "INFO",
                    "output_to_file": True
                }
            }
        }
    }
    
    pipeline_config_file = config_path / "demo_amm_pipeline.yaml"
    with open(pipeline_config_file, "w", encoding="utf-8") as f:
        yaml.dump(pipeline_config, f)
    
    logger.info(f"Created pipeline configuration: {pipeline_config_file}")
    
    return kdb_root, output_path, pipeline_config_file


def run_pipeline_demo():
    """Run the complete pipeline demonstration."""
    print_banner()
    
    logger.info("=" * 70)
    logger.info("S1000D AMM Content Pipeline Demo")
    logger.info("=" * 70)
    
    # Setup demo environment
    base_path = Path.cwd() / "demo_run"
    base_path.mkdir(exist_ok=True)
    
    kdb_root, output_path, pipeline_config_file = setup_demo_environment(base_path)
    
    logger.info("")
    logger.info("Demo Environment Setup Complete:")
    logger.info(f"  KDB Root: {kdb_root}")
    logger.info(f"  Output Path: {output_path}")
    logger.info(f"  Pipeline Config: {pipeline_config_file}")
    logger.info("")
    
    # Method 1: Using convenience function
    logger.info("-" * 70)
    logger.info("Method 1: Using execute_pipeline() convenience function")
    logger.info("-" * 70)
    
    try:
        result = execute_pipeline(
            pipeline_yaml=pipeline_config_file,
            contract_id="DEMO-CONTRACT-001",
            baseline_id="DEMO-BASELINE-001",
            kdb_root=kdb_root,
            output_path=output_path
        )
        
        logger.info("")
        logger.info("Pipeline Execution Results:")
        logger.info(f"  Run ID: {result.run_id}")
        logger.info(f"  Status: {result.status.value}")
        logger.info(f"  Contract: {result.contract_id}")
        logger.info(f"  Baseline: {result.baseline_id}")
        logger.info(f"  Stages Executed: {len(result.stage_results)}")
        
        if result.stage_results:
            logger.info("")
            logger.info("Stage Results:")
            for stage_result in result.stage_results:
                status_symbol = "✓" if stage_result.status.value == "COMPLETED" else "✗"
                logger.info(f"    {status_symbol} {stage_result.stage_name}: {stage_result.status.value}")
                logger.info(f"      - Artifacts: {stage_result.artifacts_produced}")
                if stage_result.errors:
                    for err in stage_result.errors:
                        logger.info(f"      - Error: {err}")
                if stage_result.warnings:
                    for warn in stage_result.warnings:
                        logger.info(f"      - Warning: {warn}")
        
        logger.info("")
        logger.info("Outputs Generated:")
        if output_path.exists():
            for item in output_path.rglob("*"):
                if item.is_file():
                    logger.info(f"  ✓ {item.relative_to(output_path)}")
        
        logger.info("")
        logger.info("=" * 70)
        logger.info("Demo completed successfully!")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        return False


def main():
    """Main entry point."""
    try:
        success = run_pipeline_demo()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Demo cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
