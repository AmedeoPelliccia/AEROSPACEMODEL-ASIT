# I-INFRASTRUCTURES Index

## Subdomain Structure

| Subdomain | Code | Categories | Description |
|-----------|------|------------|-------------|
| Manufacturing Facilities | **M1** | ATA 85 | Production lines, test rigs, assembly benches |
| Maintenance Environments | **M2** | ATA 08I, 10I, 12I | In-line, hangars, shops |
| Operations & Service Structures | **O** | ATA 03I, ATA IN H₂ GSE | Airport facilities, fuel logistics, ground services |

---

## M1 — Manufacturing Facilities

Factory-floor infrastructure for production and assembly organized by functional standards and regulations.

| Subdomain | Code | Description |
|-----------|------|-------------|
| Quality | 01 | Quality Management System (ISO 9001, AS9100, NADCAP, AS9102) |
| OHS Safety Workplace | 02 | Occupational Health & Safety (ISO 45001, OSHA, ES RD 486/1997) |
| Environment HAZMAT | 03 | Environmental & Hazardous Materials (ISO 14001, REACH/CLP, NFPA 2/55) |
| Machinery Process Safety | 04 | Machinery & Process Safety (ISO 12100, ISO 13849) |
| Warehouse Inventory | 05 | Inventory & Logistics (RFID/QR Traceability, ISO 17025) |
| Additive Manufacturing | 06 | AM Quality Gates, Powder Traceability, NADCAP |
| Airworthiness Production | 07 | POA/PC (EASA Part 21 Subpart G, FAA 14 CFR Part 21) |
| Templates Meta | 90 | `.meta.yaml` templates and JSON Schema |
| References | 99 | External standards and regulations links |

**ATA Designation:** 85-00-00 (Manufacturing Facilities)  
**Structure:** Standards-based subdomains (01-07, 90, 99) rather than ATA-chapter directories  
**Details:** See `M1-MANUFACTURING_FACILITIES/README.md` and `M1-MANUFACTURING_FACILITIES/00_INDEX.md`

## M2 — Maintenance Environments

Maintenance ecosystem from line stations through heavy-maintenance hangars to component shops.

| Category | Directory | Description |
|----------|-----------|-------------|
| Weighing | `M2-MAINTENANCE_ENVIRONMENTS/ATA_08-LEVELING_AND_WEIGHING_INFRA/` | Leveling and weighing facilities |
| Ground Handling | `M2-MAINTENANCE_ENVIRONMENTS/ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/` | Parking, mooring, and storage infrastructure |
| Servicing | `M2-MAINTENANCE_ENVIRONMENTS/ATA_12-SERVICING_INFRA/` | Servicing equipment and fluid handling |

## O — Operations & Service Structures

Operational airport and logistics infrastructure including the H₂ supply chain.

| Category | Directory | Description |
|----------|-----------|-------------|
| Support | `O-OPERATIONS_SERVICE_STRUCTURES/ATA_03-SUPPORT_INFRA/` | Ground support equipment and tooling |
| **Hydrogen** ⭐ | `O-OPERATIONS_SERVICE_STRUCTURES/ATA_IN_H2_GSE_AND_SUPPLY_CHAIN/` | **H2 refueling, storage, and supply chain** |

---

⭐ = Novel Technology Infrastructure for hydrogen systems

*6 infrastructure categories across 3 subdomains supporting aircraft operations and novel technologies*
