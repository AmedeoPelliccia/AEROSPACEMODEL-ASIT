# S1000D Template Guide

This directory contains starter S1000D Issue 5.0 XML templates used by the ASIGT content pipeline to generate Aircraft Maintenance Manual (AMM) data modules and publications.

## Templates
- `dm_descriptive.xml` – baseline for descriptive DMs (info code 040A) such as system overviews.
- `dm_procedural.xml` – baseline for maintenance procedures (info code 520A) covering removal/installation.
- `dm_fault_isolation.xml` – baseline for troubleshooting/fault isolation DMs (info code 720A).
- `dm_ipd.xml` – baseline for Illustrated Parts Data (info code 941A).
- `pm_structure.xml` – publication module scaffold that organizes DM references.
- `dml_structure.xml` – data module list scaffold for cataloging all DMs in a publication.

Each template includes required S1000D namespaces, schema locations, security classification, and placeholder content blocks for titles, identification, and applicability.

## How to use
1) Copy the template that matches your DM type.  
2) Update the Data Module Code (DMC) fields (model, ATA chapter, sub-system, info code).  
3) Replace placeholder titles, content sections, and figure references with authoritative data.  
4) Validate against the S1000D 5.0 schema (e.g., `xmllint --noout --schema S1000D_5-0/xml_schema_flat/descript.xsd dm.xml`).  
5) Add the resulting DMs to your publication module and DML using `pm_structure.xml` and `dml_structure.xml`.

## Pipeline integration
- The ASIGT content pipeline (`src/aerospacemodel/asigt/pipeline.py`) uses these templates when transforming normalized KDB inputs into S1000D outputs.
- The demo runner (`examples/run_amm_pipeline_demo.py`) shows the end-to-end flow from KDB creation through DM/PM/DML generation and CSDB assembly.
- Example populated files are provided in `examples/` for ATA 27 (Flight Controls) and ATA 28 (Fuel).

## Related documentation
- [Content Pipeline Documentation](../../docs/CONTENT_PIPELINE.md)
- [S1000D Template Examples](examples/README.md)
- [ASIGT Pipeline Implementation](../../src/aerospacemodel/asigt/pipeline.py)
