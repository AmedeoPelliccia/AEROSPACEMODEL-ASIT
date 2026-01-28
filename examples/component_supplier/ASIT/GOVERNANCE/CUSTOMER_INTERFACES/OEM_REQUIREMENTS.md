# OEM Customer Interface Requirements

## Overview

This document defines the interface requirements for each OEM customer receiving LGA-5000 documentation.

## OEM-A (Aircraft Type-X)

### Contact Information

| Role | Name | Email |
|------|------|-------|
| Technical Publications | J. Smith | j.smith@oem-a.example |
| Configuration Management | R. Jones | r.jones@oem-a.example |
| Engineering | T. Brown | t.brown@oem-a.example |

### Document Requirements

| Requirement | Value |
|-------------|-------|
| S1000D Issue | 5.0 |
| BREX | OEM-A-BREX-2025 |
| Language | English (US) |
| Delivery Format | CSDB + PDF |
| Delivery Method | Secure portal upload |

### Part Number Mapping

| Supplier P/N | OEM-A P/N | Description |
|--------------|-----------|-------------|
| LGA-5000-100 | OEM-A-32-4001 | Main Gear Actuator |
| LGA-5000-200 | OEM-A-32-4002 | Nose Gear Actuator |

### Effectivity

| P/N | Aircraft | MSN Range |
|-----|----------|-----------|
| LGA-5000-100 | Type-X | 001-500 |
| LGA-5000-200 | Type-X | 001-500 |

### Change Notification

- **Lead time:** 90 days minimum
- **Format:** OEM-A Change Notification Form (CNF)
- **Approval:** Required before implementation

---

## OEM-B (Aircraft Type-Y)

### Contact Information

| Role | Name | Email |
|------|------|-------|
| Supplier Documentation | M. Lee | m.lee@oem-b.example |
| Quality Assurance | S. Park | s.park@oem-b.example |

### Document Requirements

| Requirement | Value |
|-------------|-------|
| S1000D Issue | 5.0 |
| BREX | OEM-B-BREX-R3 |
| Language | English (UK) + French |
| Delivery Format | CSDB only |
| Delivery Method | API integration |

### Part Number Mapping

| Supplier P/N | OEM-B P/N | Description |
|--------------|-----------|-------------|
| LGA-5000-150 | OEM-B-LG-001 | Main Gear Actuator |
| LGA-5000-250 | OEM-B-LG-002 | Nose Gear Actuator |

### Effectivity

| P/N | Aircraft | MSN Range |
|-----|----------|-----------|
| LGA-5000-150 | Type-Y | 001-300 |
| LGA-5000-250 | Type-Y | 001-300 |

### Change Notification

- **Lead time:** 120 days minimum
- **Format:** OEM-B Supplier Change Request (SCR)
- **Approval:** Required before production

---

## Common Requirements

### Quality Documentation

All customers require:
- First Article Inspection (FAI) reports
- Certificates of Conformance (CoC)
- Material certifications
- Test reports

### Service Bulletin Distribution

| SB Type | Notification | Implementation |
|---------|--------------|----------------|
| Mandatory | Immediate | Per OEM schedule |
| Optional | 30 days | Per operator |
| Alert | Immediate | Immediate grounding |

### Revision Delivery Schedule

| Publication | Frequency |
|-------------|-----------|
| CMM | Per change + annual |
| IPC | Per change + annual |
| SB | As required |
