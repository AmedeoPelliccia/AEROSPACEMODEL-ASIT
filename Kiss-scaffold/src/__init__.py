"""
Aircraft GenKISS — General Knowledge and Information Standard Systems

Deterministic scaffold generator for aerospace repositories with:

- GENESIS: Knowledge Determination Space
- SSOT: Authoritative Information Source
- PUB/ATDP: Aircraft Technical Data Product publication umbrella
- 00-90: Tables, Schemas, and Index governance layer
"""

from .cli import parse_args, parse_timestamp
from .config_loader import CANONICAL_ORDER, ConfigError, load_configs
from .generator import (
    GenContext,
    GenerationError,
    gen_root,
    gen_genesis,
    gen_ssot,
    gen_csdb_pub,
    gen_0090,
)
from .validator import ValidationError, validate_locked_rules_and_lifecycle
from .utils import write_manifest

__all__ = [
    # metadata
    "__version__",
    "__tool_name__",
    "__description__",
    # cli
    "parse_args",
    "parse_timestamp",
    # config
    "CANONICAL_ORDER",
    "ConfigError",
    "load_configs",
    # generation
    "GenContext",
    "GenerationError",
    "gen_root",
    "gen_genesis",
    "gen_ssot",
    "gen_csdb_pub",
    "gen_0090",
    # validation
    "ValidationError",
    "validate_locked_rules_and_lifecycle",
    # utils
    "write_manifest",
]

__version__ = "1.0.0"
__tool_name__ = "Aircraft GenKISS"
__description__ = (
    "General Knowledge and Information Standard Systems scaffold generator "
    "for aerospace project structures."
)
