# SkyLift-200 — Special Conditions

## Overview

The SkyLift-200 is certified under **14 CFR Part 23 Amendment 64** with the following Special Conditions to address novel and unusual design features.

## Special Conditions Summary

| SC Number | Title | Status |
|-----------|-------|--------|
| SC-VTOL-01 | High-Voltage Electrical Systems | In Progress |
| SC-VTOL-02 | Distributed Propulsion | In Progress |
| SC-VTOL-03 | Battery Fire Protection | In Progress |
| SC-VTOL-04 | CSFL for DEP | Planned |
| SC-VTOL-05 | Autonomous Flight Functions | Future |
| SC-VTOL-06 | Cyber Security | In Progress |

---

## SC-VTOL-01: High-Voltage Electrical Systems

### Applicability
800V DC electrical power system and associated components.

### Requirement
The high-voltage electrical system must:
1. Protect occupants and maintenance personnel from electrical hazards
2. Provide adequate electrical isolation
3. Include arc fault protection
4. Maintain functionality after single failures

### Means of Compliance
- Analysis: FMEA, FTA, EWIS analysis
- Test: High-pot testing, isolation testing
- Inspection: Wire routing inspection

### Documentation
- AMM procedures for HV system maintenance
- Warning/caution placards
- Personal protective equipment requirements

---

## SC-VTOL-02: Distributed Propulsion

### Applicability
Eight (8) electric motor propulsion units.

### Requirement
The distributed electric propulsion system must:
1. Maintain controlled flight with any two adjacent motor failures
2. Provide equivalent safety to conventional twin-engine aircraft
3. Include motor health monitoring

### Means of Compliance
- Analysis: Rotor-out performance analysis
- Simulation: 6-DOF simulation with failures
- Flight Test: Simulated motor-out testing

### Documentation
- Normal procedures for all-motor operation
- Abnormal procedures for motor failure
- Performance data for degraded operation

---

## SC-VTOL-03: Battery Fire Protection

### Applicability
Lithium-ion battery packs (160 kWh total capacity).

### Requirement
The battery installation must:
1. Contain thermal runaway propagation
2. Prevent fire from affecting flight-critical systems
3. Provide crew warning of thermal events
4. Allow safe evacuation after ground thermal event

### Means of Compliance
- Test: Cell-level thermal runaway testing
- Test: Pack-level propagation testing
- Analysis: Thermal modeling

### Documentation
- Emergency procedures for battery fire
- Ground handling procedures
- Maintenance inspection procedures

---

## SC-VTOL-04: Continued Safe Flight and Landing (CSFL)

### Applicability
All flight-critical systems with novel failure modes.

### Requirement
Following any single failure or combination of failures not shown to be extremely improbable, the aircraft must be capable of continued safe flight and landing.

### Means of Compliance
- Analysis: CSFL failure analysis
- Simulation: Failure injection simulation
- Flight Test: Simulated failure flight test

---

## SC-VTOL-05: Autonomous Flight Functions

### Applicability
(Future) Autonomous flight capability (SL2-A variant).

### Requirement
Reserved for autonomous operation certification.

### Status
Not currently in scope. Will be addressed in future certification program.

---

## SC-VTOL-06: Cyber Security

### Applicability
All programmable electronic systems.

### Requirement
The aircraft must be protected against unauthorized electronic access that could affect safety of flight.

### Means of Compliance
- Analysis: Threat assessment
- Design: Security architecture review
- Test: Penetration testing

### Documentation
- Security Architecture Document
- Cyber Security Plan
- Incident Response Procedures
