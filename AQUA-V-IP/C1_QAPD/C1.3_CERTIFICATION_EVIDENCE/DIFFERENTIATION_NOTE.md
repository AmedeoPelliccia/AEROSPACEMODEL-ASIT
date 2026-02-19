# Differentiation Note — C1.3 Automated Certification Evidence Generation

**Docket:** AQUA-V-C1.3-2026-001  
**Date:** 2026-02-19

---

## 1. Technical Problem Solved

C1.3 solves the **last-mile certification problem** for quantum-assisted aerospace design: even when DERs (C1.2) are available, generating a certification package that is acceptable to EASA or FAA requires: domain knowledge of applicable standards (CS-25, DO-178C, ARP4754A), traceability linkage to requirements and design decisions, and a legally valid electronic signature. C1.3 automates this process.

## 2. Why the Solution Is Non-Obvious

1. **eIDAS-qualified signature on quantum evidence** is non-obvious: eIDAS is an EU electronic signature regulation; applying it to quantum computation outputs requires understanding both EU law and quantum computing, a combination not found in any prior art
2. **Automated traceability from `lc_phase` → DO-178C objectives** requires a mapping that is not documented anywhere; it is a contribution of C1.3
3. The **natural language summary generation** for certification engineers (Claim 7) addresses a non-obvious human factors problem: most certification engineers have no quantum computing background and cannot interpret a raw DER

## 3. Inventive Step Beyond Closest Prior Art

The Autodesk reference (closest prior art) generates certification-ready documentation from classical simulation. C1.3 extends this to quantum computation by adding:
- DER integrity verification before packaging
- Automated DO-178C / ARP4754A objective mapping
- eIDAS-qualified signature (EU regulatory alignment)
- Natural language summary for certification engineers

## 4. Connection to AQUA-V Architecture

C1.3 is the **regulatory interface layer** of QAPD. It connects the AQUA-V evidence chain (produced by C1.2) to the external regulatory system (EASA DOA, FAA type certificate). Without C1.3, the DERs are technically sound but not formatted for regulatory consumption. With C1.3, AQUA-V provides an **end-to-end path from quantum computation to certification authority**.

The eIDAS-qualified signature is specifically motivated by the EU framework mandate: all IP and regulatory submissions from the AQUA-V system must be signed with EU-recognised qualified electronic signatures to maximise legal standing before EASA.
