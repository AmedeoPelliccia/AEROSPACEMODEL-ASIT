# NGI Policy Compliance System

This directory contains the NGI (Next Generation Internet) policy compliance system for automated assessment and enforcement of trust, security, and governance standards.

## Overview

The NGI policy system provides deterministic, CI/CD-integrated compliance checking across 9 domains:

1. **D1_verificability**: Claims traceability and verification
2. **D2_transparency**: Documentation and system cards
3. **D3_privacy**: Data protection and legal basis
4. **D4_security**: Security controls and testing
5. **D5_governance**: Decision-making and approval processes
6. **D6_interop**: Standards compliance and data portability
7. **D7_identity**: Legal entity verification
8. **D8_sustainability**: Environmental and resource metrics
9. **D9_antimisinf**: Claim risk assessment and validation

## Scoring System

Each domain is scored on a 0-5 scale:

- **0**: Inexistente (non-existent)
- **1**: Ad-hoc (informal)
- **2**: Básico documentado (basic, documented)
- **3**: Implementado repetible (implemented, repeatable)
- **4**: Medido con KPIs (measured with KPIs)
- **5**: Optimizado auditado externamente (optimized, externally audited)

## Decision Logic

The system produces three possible decisions:

### PASS ✅
- All hard gates passed (D1, D3, D4, D7 >= 3)
- All domains >= 2
- Total weighted score >= 70

### WARN ⚠️
- All hard gates passed
- All domains >= 2
- Total weighted score < 70

### BLOCK 🛑
- Any hard gate failed (D1, D3, D4, or D7 < 3)
- OR any domain < 2

## Files

- `ngi_policy_v1.yaml`: Policy definition with scoring rules and gates
- `README.md`: This file

## Usage

The policy is enforced via `.github/workflows/ngi-assessment.yml` which runs on pull requests. Projects must provide an assessment file at `assessments/ngi_assessment.yaml`.

See `assessments/ngi_assessment.template.yaml` for the assessment structure.

## Maturity Levels

Based on total weighted score (0-100):

- **L1** (0-39): Inicial Reactivo
- **L2** (40-59): Control Básico
- **L3** (60-74): Operación Gobernada
- **L4** (75-89): Gestión Avanzada con Métricas
- **L5** (90-100): Referencia Auditable

## Evidence Requirements

Each domain requires at least 1 piece of evidence. Evidence can be:

- File paths in the repository
- External URLs to documentation
- References to compliance artifacts

## Deployment Semantics

- **PASS**: Automatic deployment + trust badge
- **WARN**: Allow PR merge but block production deployment
- **BLOCK**: Block PR merge and all deployment

## Version History

- **v1.0.0** (2026-02-12): Initial release
