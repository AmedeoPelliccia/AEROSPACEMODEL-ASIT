from pathlib import Path
from src.generator import GenContext, gen_root, gen_genesis, gen_ssot, gen_csdb_pub, gen_0090
from src.validator import validate_locked_rules_and_lifecycle

def test_roundtrip_generation_and_validation(tmp_path: Path):
    phases = {
        "_ordered_lc_ids": [
            "LC01_PROBLEM_STATEMENT","LC02_SYSTEM_REQUIREMENTS","LC03_SAFETY_RELIABILITY","LC04_DESIGN_DEFINITION",
            "LC05_ANALYSIS_MODELS","LC06_VERIFICATION","LC07_QA_PROCESS","LC08_CONFIGURATION",
            "LC09_ESG_SUSTAINABILITY","LC10_INDUSTRIAL_SUPPLY","LC11_OPERATIONS_CUSTOMIZATION",
            "LC12_MAINTENANCE_REPAIR","LC13_MAINTENANCE_SOURCE","LC14_END_OF_LIFE"
        ],
        "LC01_PROBLEM_STATEMENT": {"phase_type": "PLM", "canonical_name": "Problem Statement", "ssot_dir": "x/LC01"},
        "LC02_SYSTEM_REQUIREMENTS": {"phase_type": "PLM", "canonical_name": "System Requirements", "ssot_dir": "x/LC02"},
        "LC03_SAFETY_RELIABILITY": {"phase_type": "PLM", "canonical_name": "Safety & Reliability", "ssot_dir": "x/LC03"},
        "LC04_DESIGN_DEFINITION": {"phase_type": "PLM", "canonical_name": "Design Definition", "ssot_dir": "x/LC04"},
        "LC05_ANALYSIS_MODELS": {"phase_type": "PLM", "canonical_name": "Analysis Models", "ssot_dir": "x/LC05"},
        "LC06_VERIFICATION": {"phase_type": "PLM", "canonical_name": "Integration & Test", "ssot_dir": "x/LC06"},
        "LC07_QA_PROCESS": {"phase_type": "PLM", "canonical_name": "QA & Process Compliance", "ssot_dir": "x/LC07"},
        "LC08_CONFIGURATION": {"phase_type": "PLM", "canonical_name": "Certification", "ssot_dir": "x/LC08"},
        "LC09_ESG_SUSTAINABILITY": {"phase_type": "PLM", "canonical_name": "ESG & Sustainability", "ssot_dir": "x/LC09"},
        "LC10_INDUSTRIAL_SUPPLY": {"phase_type": "PLM", "canonical_name": "Industrial & Supply Chain", "ssot_dir": "x/LC10"},
        "LC11_OPERATIONS_CUSTOMIZATION": {"phase_type": "OPS", "canonical_name": "Operations Customization", "ssot_dir": "x/LC11"},
        "LC12_MAINTENANCE_REPAIR": {"phase_type": "OPS", "canonical_name": "Continued Airworthiness & MRO", "ssot_dir": "x/LC12"},
        "LC13_MAINTENANCE_SOURCE": {"phase_type": "OPS", "canonical_name": "Maintenance Source Data", "ssot_dir": "x/LC13"},
        "LC14_END_OF_LIFE": {"phase_type": "OPS", "canonical_name": "End of Life", "ssot_dir": "x/LC14"},
    }
    atdp = {"products": ["AMM", "IPC"], "common_csdb_dirs": ["DM", "PM"]}

    ctx = GenContext(base=tmp_path, mode="overwrite", now_iso="2026-02-16T10:00:00Z", date_short="2026-02-16", written=[])
    gen_root(ctx)
    gen_genesis(ctx)
    gen_ssot(ctx, phases)
    gen_csdb_pub(ctx, atdp)
    gen_0090(ctx, phases, atdp)

    ok, errs = validate_locked_rules_and_lifecycle(tmp_path, phases, atdp)
    assert ok, errs
