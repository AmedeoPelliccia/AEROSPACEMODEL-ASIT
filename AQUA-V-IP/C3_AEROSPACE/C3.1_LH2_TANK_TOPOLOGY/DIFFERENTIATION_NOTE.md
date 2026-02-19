# Differentiation Note — C3.1 LH₂ Tank Topology Optimisation

**Docket:** AQUA-V-C3.1-2026-001  
**Date:** 2026-02-19

---

## 1. Technical Problem Solved

C3.1 solves the specific problem of **optimising structural topology for cryogenic hydrogen fuel tanks** where both the discrete nature of material selection and the physical severity of cryogenic constraints make classical continuous topology optimisation inapplicable. The combination of QUBO + cryogenic penalty terms + H₂ compatibility penalty terms + ATA 28 routing compatibility penalty terms is unique to this application.

## 2. Why the Solution Is Non-Obvious

1. **Cryogenic penalty coefficient derived from thermal stress severity function** — not heuristic. The penalty coefficient must be physically calibrated to the thermomechanical behaviour at −253°C, which requires aerospace materials engineering knowledge not present in any quantum computing reference
2. **Galvanic coupling penalty for H₂-compatible material pairs** — this is a hydrogen-specific failure mode (galvanic corrosion of H₂-compatible alloy liners in contact with dissimilar metals) that is not in any QUBO literature
3. **ATA 28 routing compatibility penalty** — requires knowledge of the fuel distribution system topology (ATA 28-22 transfer lines) to formulate the routing conflict penalty

## 3. Inventive Step Beyond Closest Prior Art

Closest: Springer 2024 QUBO for aircraft loads. That reference uses binary variables for load path selection, not material selection + topology + cryogenic + compatibility. C3.1 adds four domain-specific penalty term types that require specialist knowledge of LH₂ aircraft design.

## 4. Connection to AQUA-V Architecture

C3.1 is the **most domain-specific child application**. It depends on C1.1 (hybrid QUBO encoding with aerospace constraints), C1.2 (DER for certification traceability), and C2.3 (evidence ledger for EASA DOA). It demonstrates the full AQUA-V pipeline in a concrete aerospace application that no competitor is likely to replicate without licensing the parent P0 and children C1.1 + C1.2.
