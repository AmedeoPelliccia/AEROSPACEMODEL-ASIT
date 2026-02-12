# AEROSPACEMODEL Specification Documents

This directory contains generators for formal AEROSPACEMODEL specification documents.

## NIB Technical Specification

The **Non-Inference Boundary (NIB) Technical Specification** (Document ID: `AEROSPACEMODEL-ASIT-NIB-SPEC-001`) defines the concept, classification, detection logic, escalation protocol, and evidence requirements for Non-Inference Boundaries within the AEROSPACEMODEL framework.

### What is a Non-Inference Boundary?

A Non-Inference Boundary (NIB) is the precise point in a governed automation chain where the system's deterministic reasoning capability is exhausted and human cognitive authority must be engaged to resolve irreducible ambiguity.

Unlike conventional Human-in-the-Loop (HITL) checkpoints—which are placed at arbitrary process milestones—NIBs are **structurally derived properties** of transformation contracts. They emerge where the BREX decision cascade cannot deterministically resolve an operation, making human oversight a consequence of epistemic limits rather than procedural ceremony.

### Key Features

- **Structurally Derived**: NIBs are automatically identified based on the transformation contract and BREX rules
- **Falsifiable**: Each NIB is a verifiable claim that the system cannot produce deterministic output
- **Traceable**: Full provenance from input → BREX cascade → NIB trigger → human decision → output
- **Compliant**: Implements EU AI Act Articles 14–15 and EASA AI Roadmap 2.0 requirements

### Document Generation

#### Prerequisites

- Node.js >= 16.0.0
- npm (comes with Node.js)

#### Installation

```bash
cd docs/specifications
npm install
```

#### Generate the Document

```bash
npm run generate
```

This will create `AEROSPACEMODEL-ASIT-NIB-SPEC-001.docx` in the current directory.

#### Manual Generation

```bash
node generate_nib_spec.js
```

### Document Structure

The generated specification includes:

1. **Cover Page** - Document identification, version, classification, authorship
2. **Document Control** - Revision history and approval signatures
3. **Table of Contents** - Automatically generated with hyperlinks
4. **Section 1: Scope and Purpose** - NIB concept and objectives
5. **Section 2: Definitions** - Terminology and abbreviations
6. **Section 3: Concept of Operations** - Problem statement and solution approach
7. **Section 4: NIB Classification Taxonomy** - Classification axes and matrix
8. **Section 5: Detection and Escalation** - Runtime detection and escalation protocol
9. **Section 6: Implementation Guidelines** - Technical implementation guidance
10. **Section 7: Regulatory Compliance** - EU AI Act and EASA alignment
11. **Section 8: Conclusion** - Summary and living document statement
12. **Appendices** - Example scenarios and BREX rule templates

### Integration with AEROSPACEMODEL

The NIB specification is normatively referenced by:

- **ASIT Core** (`ASIT/ASIT_CORE.md`) - Core authority framework
- **BREX Decision Engine** (`ASIGT/brex/brex_decision_engine.py`) - Runtime implementation
- **CNOT Architecture** (`docs/CNOT_AGENT_LIFECYCLE_ARCHITECTURE.md`) - Lifecycle gates
- **Master BREX Authority** (`ASIT/GOVERNANCE/master_brex_authority.yaml`) - Decision rules
- **HCDS Charter** (`Governance/HUMAN_CENTRIC_DIGITAL_SYSTEMS_CHARTER_v1.0.md`) - Human oversight principles

### Compliance Framework

The NIB specification ensures compliance with:

- **EU AI Act** (Regulation EU 2024/1689) - Articles 14–15 (Human Oversight)
- **EASA AI Roadmap 2.0** - Explainability, traceability, human oversight requirements
- **ARP4754A** - Development of Civil Aircraft and Systems
- **ARP4761** - Safety Assessment Process
- **DO-178C** - Software Considerations in Airborne Systems

### Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-13 | A. Pelliccia | Initial release |

### License

© 2026 Amedeo Pelliccia / IDEALEeu Enterprise

Licensed under the Apache License, Version 2.0. See the LICENSE file in the repository root for details.

### Related Documentation

- [ASIT Core Specification](../../ASIT/ASIT_CORE.md)
- [BREX Decision Engine](../../ASIGT/brex/brex_decision_engine.py)
- [CNOT Gates Architecture](../CNOT_GATES_ARCHITECTURE.md)
- [HCDS Charter](../../Governance/HUMAN_CENTRIC_DIGITAL_SYSTEMS_CHARTER_v1.0.md)
- [Ontology Diagram](../ONTOLOGY_DIAGRAM.md)

### Support

For questions or issues regarding the NIB specification or document generation:
- Review the specification document itself for detailed technical content
- Consult the ASIT governance documentation
- Refer to the BREX decision engine implementation

---

**Document Generator Version**: 1.0.0  
**Specification Version**: 1.0 DRAFT  
**Last Updated**: 2026-02-13
