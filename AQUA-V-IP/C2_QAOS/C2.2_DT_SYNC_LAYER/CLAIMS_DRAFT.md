# Claims Draft — C2.2 Digital Twin Synchronisation Layer

**Docket:** AQUA-V-C2.2-2026-001  
**Date:** 2026-02-19  
**Style:** EPO format (EU-first)

---

## CLAIMS

### Independent Claim 1 — Method

**1.** A computer-implemented method for synchronising an operational digital twin of a safety-critical system, the method comprising:

(a) receiving a digital twin update request comprising a proposed new value for at least one parameter of the digital twin and a provenance reference identifying at least one of: a cryptographic evidence record of a computation that produced the proposed new value; or a design record in a Single Source of Truth (SSOT) repository that authorises the proposed new value;

(b) verifying the provenance reference by: if the provenance reference identifies a cryptographic evidence record, verifying the digital signature of the evidence record and confirming that the proposed new value is derivable from the top-k results stored in the evidence record; or if the provenance reference identifies an SSOT design record, verifying that the SSOT record has the required approval status;

(c) determining a governance classification of the proposed update based on the safety criticality indicator associated with the computation or design decision identified by the provenance reference;

(d) if the governance classification corresponds to a safety-critical update: requesting human approval before modifying the digital twin state; and recording the human approval identifier in a state transition record; otherwise, applying the proposed new value to the digital twin state without human approval;

(e) creating a state transition record that binds: the parameter path modified; the previous value and new value; the verified provenance reference; the human approval identifier (if applicable); and a cryptographic hash of all transition record fields; and

(f) persisting the updated digital twin state and the state transition record in a governed digital twin data store.

---

### Dependent Claims

**2.** The method of claim 1, wherein the digital twin maintains two independently accessible fidelity levels: a first design fidelity level synchronised exclusively from validated SSOT design records; and a second operational fidelity level continuously updated from sensor data and quantum-assisted computation results; wherein state transition records distinguish the fidelity level affected by each update.

**3.** The method of claim 1, wherein a proposed update for which no valid provenance reference can be verified is rejected without modifying the digital twin state, and wherein a rejection record is created comprising the proposed update, the rejection reason, and a timestamp.

**4.** The method of claim 1, wherein the governed digital twin data store is an EU-hosted infrastructure node compliant with GAIA-X data sovereignty requirements, and wherein access to the digital twin state and state transition records is governed by an access control policy that restricts data export to jurisdictions outside the European Economic Area except under explicit data transfer agreements.

---

*Preliminary draft — EP filing at EPO (Munich, EU).*
