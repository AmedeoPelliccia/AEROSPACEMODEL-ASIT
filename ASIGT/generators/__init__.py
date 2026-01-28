# =============================================================================
# ASIGT Generators Module
# S1000D content generation under ASIT contract authority
# Version: 2.0.0
# =============================================================================
"""
ASIGT Generators Package

This package provides S1000D-compliant content generators that operate
exclusively under ASIT contract authority. No generation occurs without
a valid, approved contract specifying:
- Source baseline
- Target publication type
- Scope (ATA chapters, effectivity)
- Validation requirements
- Approval authority

Generators:
    - dm_generator: Data Module (DM) generation
    - pm_generator: Publication Module (PM) generation
    - dml_generator: Data Module List (DML) generation
    - icn_handler: Information Control Number / graphics handling
    - applicability: ACT/PCT/CCT applicability processing

Usage:
    from asigt.generators import DMGenerator, PMGenerator
    
    # All generators require an ASIT contract
    generator = DMGenerator(contract=contract, config=config)
    result = generator.generate(sources=sources)
"""

from .dm_generator import DMGenerator
from .pm_generator import PMGenerator
from .dml_generator import DMLGenerator
from .icn_handler import ICNHandler
from .applicability import ApplicabilityProcessor

__all__ = [
    "DMGenerator",
    "PMGenerator", 
    "DMLGenerator",
    "ICNHandler",
    "ApplicabilityProcessor",
]

__version__ = "2.0.0"
