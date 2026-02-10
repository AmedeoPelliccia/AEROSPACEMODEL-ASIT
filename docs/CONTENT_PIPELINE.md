# S1000D AMM Content Pipeline

## Overview

The S1000D AMM Content Pipeline is a comprehensive orchestration system that transforms engineering knowledge and technical data into deliverable S1000D-compliant Aircraft Maintenance Manual (AMM) publications.

## Pipeline Architecture

```
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
```

## Five Pipeline Stages

### 1. INGEST & NORMALIZE
**Purpose:** Load and normalize source data from multiple formats

**Responsibilities:**
- Load source data from OEM data, engineering docs, legacy documents
- Normalize data to common internal format
- Validate data completeness and consistency
- Extract metadata and relationships
- Compute input hashes for traceability

**Inputs:**
- Requirements (YAML, JSON, XML)
- Maintenance tasks
- Fault isolation data
- Schematics and graphics
- Part data

**Outputs:**
- Normalized source artifacts
- Input manifest
- Source metadata

### 2. VALIDATE & ENRICH
**Purpose:** Apply business rules and enrich content

**Responsibilities:**
- Apply BREX business rules
- Schema validation
- Enrich content with cross-references
- Add applicability information
- Validate data quality
- Generate warnings for potential issues

**Validations:**
- Required fields present
- ATA chapter assigned
- Data completeness
- Business rule compliance

**Enrichment:**
- Cross-references between artifacts
- Applicability tagging
- Timestamp metadata
- Source traceability

### 3. TRANSFORM TO S1000D
**Purpose:** Transform normalized data to S1000D Data Modules

**Responsibilities:**
- Apply XSLT/mapping rules
- Generate Data Modules (DM)
- Generate DMC (Data Module Code) codes
- Apply SNS coding
- Handle ICN (graphics) references
- Link cross-references

**DM Types Generated:**
- Descriptive DMs (from requirements)
- Procedural DMs (from tasks)
- Fault Isolation DMs (from troubleshooting data)
- Schematic DMs
- IPD (Illustrated Parts Data)

**Outputs:**
- S1000D XML Data Modules
- ICN files
- DMC registry

### 4. ASSEMBLE DATA MODULES
**Purpose:** Assemble DMs into publication structure

**Responsibilities:**
- Assemble DMs into CSDB structure
- Generate Publication Module (PM)
- Generate Data Module List (DML)
- Apply applicability filtering
- Build publication TOC structure
- Organize by ATA chapters

**Outputs:**
- Publication Module (PM)
- Data Module List (DML)
- CSDB package structure
- Applicability tables

### 5. PUBLISH & QA
**Purpose:** Render outputs and perform quality assurance

**Responsibilities:**
- Render to deliverable formats (IETP, PDF, IETM)
- Perform quality assurance checks
- Generate validation reports
- Package for delivery
- Create delivery manifests

**Output Formats:**
- IETP (Interactive Electronic Technical Publication)
- PDF (Portable Document Format)
- HTML (Web-based viewer)
- IETM (Interactive Electronic Technical Manual)

**QA Checks:**
- All DMs have valid DMC codes
- All cross-references resolve
- All ICN files exist
- No orphaned artifacts
- Schema compliance

## Usage

### Basic Usage

```python
from pathlib import Path
from aerospacemodel.asigt.pipeline import execute_pipeline

# Execute pipeline with simplified interface
result = execute_pipeline(
    pipeline_yaml=Path("pipelines/amm_pipeline.yaml"),
    contract_id="KITDM-CTR-LM-CSDB_ATA28",
    baseline_id="FBL-2026-Q1-003",
    kdb_root=Path("KDB"),
    output_path=Path("IDB/CSDB/AMM")
)

# Check results
if result.status.value == "SUCCESS":
    print(f"✓ Pipeline completed successfully")
    print(f"  Generated {result.output_count} artifacts")
    print(f"  Trace coverage: {result.trace_coverage:.1f}%")
else:
    print(f"✗ Pipeline failed: {result.status.value}")
    for error in result.errors:
        print(f"  - {error}")
```

### Advanced Usage

```python
from aerospacemodel.asigt.pipeline import ContentPipeline
from aerospacemodel.asigt.engine import ExecutionContext
from datetime import datetime

# Load pipeline configuration
pipeline = ContentPipeline.from_yaml("pipelines/amm_pipeline.yaml")

# Validate configuration
is_valid, errors = pipeline.validate_config()
if not is_valid:
    print(f"Pipeline configuration errors: {errors}")
    exit(1)

# Build execution context
context = ExecutionContext(
    contract_id="KITDM-CTR-LM-CSDB_ATA28",
    contract_version="1.0",
    baseline_id="FBL-2026-Q1-003",
    authority_reference="ASIT-APPROVED",
    invocation_timestamp=datetime.now(),
    kdb_root=Path("KDB"),
    idb_root=Path("IDB"),
    output_path=Path("IDB/CSDB/AMM"),
    run_archive_path=Path("ASIGT/runs"),
    s1000d_version="S1000D_5.0",
    ata_chapters=["27", "28"],
    render_outputs=True
)

# Execute pipeline
result = pipeline.execute(context)

# Process stage results
for stage_result in result.stage_results:
    print(f"{stage_result.stage_name}: {stage_result.status.value}")
    print(f"  Artifacts: {stage_result.artifacts_produced}")
    print(f"  Duration: {stage_result.duration_seconds:.2f}s")
```

### Pipeline Configuration

Example `amm_pipeline.yaml`:

```yaml
pipeline:
  metadata:
    pipeline_id: "AMM-001"
    name: "Aircraft Maintenance Manual Pipeline"
    version: "2.0.0"
    publication_type: "AMM"
    
  stages:
    - stage: "initialization"
      name: "Initialize Pipeline"
      order: 1
      
    - stage: "source_loading"
      name: "Load Sources"
      order: 2
      
    - stage: "transformation"
      name: "Transform to S1000D"
      order: 3
      
    - stage: "validation"
      name: "Validate Content"
      order: 4
      
    - stage: "publication_assembly"
      name: "Assemble Publication"
      order: 5
      
    - stage: "rendering"
      name: "Render Outputs"
      order: 6
```

## Running the Demo

A complete working demo is provided:

```bash
# Run the demo
python examples/run_amm_pipeline_demo.py

# The demo will:
# 1. Create sample KDB with requirements and tasks
# 2. Execute the complete pipeline
# 3. Generate S1000D DMs, PM, and DML
# 4. Display execution results
```

## Testing

Comprehensive test suite with 24 tests:

```bash
# Run all pipeline tests
python -m pytest tests/test_content_pipeline.py -v

# Run specific test class
python -m pytest tests/test_content_pipeline.py::TestTransformStage -v

# Run with coverage
python -m pytest tests/test_content_pipeline.py --cov=aerospacemodel.asigt.pipeline
```

## Integration with ASIGT

The Content Pipeline integrates seamlessly with the ASIGT engine:

```python
from aerospacemodel import ASIT, ASIGT
from aerospacemodel.asigt.pipeline import ContentPipeline

# Initialize ASIT governance
asit = ASIT(config_path="ASIT/config/asit_config.yaml")
asigt = ASIGT(asit_instance=asit)

# Get contract
contract = asit.get_contract("KITDM-CTR-LM-CSDB_ATA28")

# Execute through ASIGT (which uses ContentPipeline internally)
result = asigt.execute(contract, baseline_id="FBL-2026-Q1-003")
```

## Pipeline Outputs

### CSDB Structure

The AssembleStage creates a proper CSDB (Common Source Database) structure and copies all artifacts into their designated subdirectories:

```
IDB/CSDB/AMM/
├── CSDB/                        # Assembled CSDB package
│   ├── DM/                      # Data Modules (copied from output_path)
│   │   ├── DMC-AERO-A-28-00-00-00A-040A-A.xml
│   │   ├── DMC-AERO-A-28-10-00-00A-520A-A.xml
│   │   └── ...
│   ├── PM/                      # Publication Modules (copied from output_path)
│   │   └── PM-AMM-2026-00001.xml
│   ├── DML/                     # Data Module Lists (copied from output_path)
│   │   └── DML-AMM-2026-00001.xml
│   └── ICN/                     # Graphics (if present)
│       ├── ICN-AERO-00001-001.cgm
│       └── ...
├── DMC-*.xml                    # Original DMs (before CSDB assembly)
├── PM-*.xml                     # Original PM
└── DML-*.xml                    # Original DML
```

**Note:** The `_assemble_csdb()` method copies DMs, PM, and DML files into the `CSDB/` subdirectory structure. Both the original files and the CSDB-organized copies are preserved.

### Run Artifacts

Every pipeline execution creates run artifacts in the configured run_archive_path (defaults to `output_path/../ASIGT/runs/`):

```
ASIGT/runs/20260210-1430__KITDM-CTR-LM-CSDB_ATA28/
├── run_metadata.json            # Run configuration and timing
├── stage_results.json           # Individual stage execution results
└── LOG.txt                      # Detailed execution log
```

**Note:** The current implementation focuses on pipeline execution and artifact generation. Full manifest and traceability matrix population is available through the ASIGT engine's extended functionality and can be integrated as needed for production deployments.

## Performance Metrics

The pipeline tracks comprehensive metrics:

- **Sources loaded:** Number of input artifacts processed
- **Outputs generated:** Number of DMs, PM, DML created
- **Trace coverage:** Percentage of source-to-output traceability
- **Validation results:** BREX, schema, trace validation pass/fail
- **Stage timings:** Duration of each pipeline stage
- **Artifact sizes:** Total size of generated content

## Error Handling

The pipeline provides comprehensive error handling:

- **FATAL errors:** Stop execution (invalid contract, missing baseline)
- **ERROR level:** Log and continue with other artifacts
- **WARNING level:** Log but don't fail
- **Validation errors:** Collected and reported in validation report

## Extension Points

### Custom Stages

Add custom pipeline stages:

```python
from aerospacemodel.asigt.pipeline import PipelineStageConfig, PipelineStageType

class CustomValidationStage:
    def __init__(self, config: PipelineStageConfig):
        self.config = config
    
    def execute(self, context, state):
        # Custom validation logic
        pass
```

### Custom Transformations

Add custom transformation rules:

```yaml
# mapping/custom_to_dm.yaml
mapping:
  name: "Custom to DM"
  field_mappings:
    - source: "custom.field"
      target: "dmTitle.techName"
      transform: "direct"
```

## Compliance

The pipeline ensures compliance with:

- **S1000D Issue 5.0:** Standard specification for data modules
- **DO-178C:** Traceability requirements for software certification
- **ARP4761:** Safety assessment for aircraft systems
- **BREX:** Business Rules Exchange for validation

## Documentation

- [ASIGT Core Specification](../ASIGT/ASIGT_CORE.md)
- [Pipeline YAML Specification](../pipelines/README.md)
- [S1000D Templates](../ASIGT/s1000d_templates/README.md)
- [BREX Rules](../ASIGT/brex/README.md)

## Support

For issues or questions:
- GitHub Issues: https://github.com/AmedeoPelliccia/AEROSPACEMODEL/issues
- Documentation: https://docs.aerospacemodel.io

## License

Apache License 2.0 - See LICENSE file for details
