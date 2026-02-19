# Prior Art Matrix — C1.2 Deterministic Reproducibility Pipelines

**Docket:** AQUA-V-C1.2-2026-001  
**Date:** 2026-02-19  
**Note:** ★ Highest priority — prior art search most critical for this application

---

| Reference | Date | What It Covers | What It Does NOT Cover (AQUA-V Gap) | Risk Level |
|---|---|---|---|---|
| **Farhi et al., QAOA** ([arXiv:1411.4028](https://arxiv.org/abs/1411.4028)) | 2014 | QAOA algorithm; variational circuit ansatz; approximate optimisation | Deterministic seeding; evidence records; cryptographic binding; certification traceability; lifecycle phase binding | Low |
| **Qiskit Aer simulator** ([Qiskit documentation](https://qiskit.github.io/qiskit-aer/)) | 2017–2025 | Seeded quantum circuit simulation; `seed_simulator` parameter; reproducible local simulation | Evidence record generation; digital signature; HSM integration; QPU non-determinism handling; regulatory compliance packaging; SSOT promotion | Medium |
| **IBM Quantum job API** ([IBM Quantum docs](https://docs.quantum.ibm.com)) | 2020–2025 | Job result retrieval; result storage in cloud backend; job ID reference | Compact evidence record; input-derived seed; cryptographic binding of seed+hash+version; offline reconstruction from record; lifecycle phase tagging | Medium |
| **DO-178C Software Considerations in Airborne Systems** (RTCA, 2011) | 2011 | Software development assurance for airborne systems; traceability requirements; tool qualification; independence requirements | Quantum-specific reproducibility mechanisms; QUBO computation evidence; deterministic seeding for probabilistic algorithms; cryptographic evidence records | Low |
| **ARP4754A System Development Guidelines** (SAE, 2010) | 2010 | Design process assurance; traceability from requirements to design; independence of verification | Quantum computation integration; evidence record format for quantum-assisted design; non-determinism handling | Low |
| **Optimised QUBO formulation methods** ([arXiv:2406.07681](https://arxiv.org/abs/2406.07681)) | 2024 | QUBO construction and optimisation; constraint satisfaction | Deterministic seeding; evidence records; cryptographic binding; certification use | Low |
| **Autodesk Certification-Ready Digital Twin** ([Autodesk Research](https://www.research.autodesk.com/publications/certification-ready-design-digital-twin-high-performance-engineering/)) | 2023 | Certification-ready design via digital twin; simulation traceability; design documentation | Quantum computation reproducibility; seeded QPU execution; cryptographic evidence record for quantum results | **High** |
| **NIST SP 800-90A (PRNG seeding)** ([NIST](https://csrc.nist.gov/publications/detail/sp/800-90a/rev-1/final)) | 2015 | Deterministic random bit generation; seed derivation; cryptographic PRNG standards | Quantum circuit seeding; QPU hardware non-determinism; aerospace certification integration; top-k result storage and verification | Low |
| **Git / Merkle tree content-addressed storage** ([multiple sources]) | 2005–2025 | Content-addressed storage; cryptographic hashing of data objects; tamper-evident linked records | Quantum computation-specific evidence; digital signature over quantum result sets; lifecycle phase binding; regulatory submission packaging | Low |
| **Digital twins in aerospace** ([Nature 2024](https://www.nature.com/articles/s43588-024-00613-8)) | 2024 | Digital twin for aerospace design; data provenance; simulation traceability | Quantum computation evidence; seeded QPU runs; deterministic evidence records for quantum results | Low |

---

## Gap Analysis Summary

The critical gap across all prior art:
> No reference discloses a method that: (1) derives a deterministic seed from the **hash of the inputs** (not from a random source), (2) records the **solver version** alongside the seed, (3) generates a **cryptographic evidence record** that allows reconstruction of top-k quantum results, AND (4) applies digital signature with HSM for tamper evidence, in a safety-critical certification context.

The Autodesk reference is the highest-risk reference because it addresses certification-ready design with traceability — but it uses classical simulation only. C1.2 must be clearly differentiated as addressing **quantum computation non-determinism**, which is a distinct technical problem.

*Full Derwent Innovation / Espacenet search to be completed by European Patent Attorney before EP filing.*
