# AEROSPACEMODEL Templates

## Program Initialization Templates

This directory contains templates used by `aerospacemodel init` to scaffold new aircraft programs with the complete ASIT-ASIGT structure.

## Directory Structure

```
templates/
└── program/                    # Full program template
    ├── README.md.j2            # Program README template
    ├── program_config.yaml.j2  # Main program configuration
    ├── asit/                   # ASIT layer templates
    │   ├── asit_config.yaml.j2
    │   ├── governance/
    │   ├── structure/
    │   ├── contracts/
    │   └── index/
    └── asigt/                  # ASIGT layer templates
        ├── asigt_config.yaml.j2
        └── brex/
```

## Usage

### CLI Initialization

```bash
# Initialize a new program
aerospacemodel init \
  --program "HydrogenJet-100" \
  --model-code "HJ1" \
  --organization "Green Aviation Inc." \
  --output ./HJ1-ASIT-ASIGT

# Initialize with specific options
aerospacemodel init \
  --program "RegionalJet-500" \
  --model-code "RJ5" \
  --organization "Regional Aircraft Corp" \
  --s1000d-issue "5.0" \
  --cage-code "ABC12" \
  --output ./RJ5-ASIT-ASIGT
```

### Programmatic Initialization

```python
from aerospacemodel import init_program

init_program(
    program_name="HydrogenJet-100",
    model_code="HJ1",
    organization="Green Aviation Inc.",
    output_path="./HJ1-ASIT-ASIGT",
    s1000d_issue="5.0",
    options={
        "cage_code": "XYZ99",
        "country_code": "US",
        "language": "en"
    }
)
```

## Template Variables

Templates use Jinja2 syntax. Available variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `program_name` | Full program name | "HydrogenJet-100" |
| `model_code` | Short model identifier | "HJ1" |
| `organization` | Organization name | "Green Aviation Inc." |
| `cage_code` | CAGE/NCAGE code | "ABC12" |
| `country_code` | ISO country code | "US" |
| `language_code` | ISO language code | "en" |
| `s1000d_issue` | S1000D issue number | "5.0" |
| `created_date` | Creation date | "2026-01-22" |
| `created_by` | Creator identifier | "system" |

## Template Types

### Configuration Templates (`.yaml.j2`)

Program and layer configuration files.

### Documentation Templates (`.md.j2`)

README and documentation files with program-specific content.

### Structure Templates

Directory scaffolds with placeholders for program-specific content.

## Customization

### Adding Custom Templates

1. Create template file in appropriate subdirectory
2. Use Jinja2 syntax for variable substitution
3. Register in `template_manifest.yaml`

### Extending Existing Templates

Templates can be extended using Jinja2 inheritance:

```jinja2
{% extends "base_config.yaml.j2" %}
{% block custom_section %}
# Custom content here
{% endblock %}
```

## Generated Structure

Running `aerospacemodel init` creates:

```
<program>/
├── README.md                   # Program documentation
├── program_config.yaml         # Master configuration
├── ASIT/
│   ├── ASIT_CORE.md
│   ├── asit_config.yaml
│   ├── GOVERNANCE/
│   │   ├── BASELINES.md
│   │   ├── BASELINE_REGISTER.csv
│   │   └── ...
│   ├── STRUCTURE/
│   ├── CONTRACTS/
│   └── INDEX/
├── ASIGT/
│   ├── ASIGT_CORE.md
│   ├── asigt_config.yaml
│   ├── generators/
│   ├── validators/
│   ├── renderers/
│   ├── brex/
│   └── runs/
└── output/                     # Generated publications
```

## Validation

Templates are validated during initialization:

- YAML syntax validation
- Required variable presence
- Schema compliance
- Cross-reference integrity

## License

Apache License 2.0 — Part of AEROSPACEMODEL
