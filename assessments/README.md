# NGI Assessments

This directory contains NGI policy assessment files for the AEROSPACEMODEL project.

## Files

- `ngi_assessment.yaml`: Current project assessment (used by CI/CD)
- `ngi_assessment.template.yaml`: Template for creating new assessments
- `ngi_assessment.result.example.yaml`: Example of a completed assessment
- `README.md`: This file

## Assessment Structure

Each assessment includes:

### Metadata
- `project_id`: Project identifier
- `assessment_date`: Date of assessment (YYYY-MM-DD)
- `assessor`: Who performed the assessment (e.g., "ci-bot", "internal")

### Domains
For each of the 9 domains (D1-D9):
- `score`: Score 0-5
- `evidence`: List of evidence items (file paths, URLs)
- `notes`: Human-readable notes

### Computed Fields
Automatically calculated by the evaluator:
- `total_score_0_100`: Weighted total score
- `maturity_level`: L1-L5 based on total score
- `hard_gates_passed`: Boolean
- `soft_gates_passed`: Boolean
- `publish_decision`: PASS, WARN, or BLOCK

### Remediation
List of actions needed to improve the assessment.

## Evidence Guidelines

### D1 - Verificability
- Claims mapping documents
- Source manifests
- Version control artifacts
- Hash/signature files

### D2 - Transparency
- Model cards
- System cards
- Architecture documentation
- Lineage traces

### D3 - Privacy
- ROPA (Record of Processing Activities)
- Retention policies
- Deletion logs
- Legal basis documentation

### D4 - Security
- Control matrix
- SAST/DAST results
- Incident response plans
- Security test results

### D5 - Governance
- Editorial policies
- Approval workflows
- Decision logs

### D6 - Interoperability
- API specifications (OpenAPI)
- Export/import specifications
- Standard compliance documents

### D7 - Identity
- Legal entity registration
- Domain verification
- Corporate documentation

### D8 - Sustainability
- Carbon footprint estimates
- Resource usage metrics
- Optimization plans

### D9 - Anti-misinformation
- Claim risk rules
- Uncertainty quantification
- Content validation policies

## Updating the Assessment

1. Copy `ngi_assessment.template.yaml` to start fresh
2. Fill in scores based on current project state
3. Add evidence file paths or URLs
4. Add explanatory notes
5. Run the evaluator to compute results:
   ```bash
   python scripts/ngi_evaluator.py \
     --policy policy/ngi_policy_v1.yaml \
     --assessment assessments/ngi_assessment.yaml \
     --out assessments/ngi_assessment.result.yaml
   ```

## Current Project Assessment

The `ngi_assessment.yaml` file reflects the current state of the AEROSPACEMODEL project:

- **Total Score**: 70/100 (L3 - Operación Gobernada)
- **Hard Gates**: ✅ Passed
- **Soft Gates**: ✅ Passed
- **Decision**: PASS ✅

### Recent Improvements

Achieved PASS status through:

1. **D8 Sustainability**: 2 → 3
   - Added per-service resource metrics
   - Documented optimization strategy
   - Established carbon impact baseline

2. **D1 Verificability**: 3 → 4
   - Implemented KPI tracking
   - Added monitoring dashboards
   - Created metrics reference

3. **D4 Security**: 3 → 4
   - Established security KPIs
   - Deployed threat monitoring
   - Documented vulnerability tracking

### Next Level: L4 (75+)

To advance to L4 (Gestión Avanzada Metricas), consider:

2. Enhance any domain with score = 3 to score = 4 by:
   - Adding KPI tracking
   - Implementing monitoring
   - Documenting metrics

## Version History

- **2026-02-12**: Initial assessment created
