#!/usr/bin/env python3
"""
AMPEL360 Q100 Identifier Grammar Example

This script demonstrates the use of the AMPEL360 Q100 controlled vocabulary
and identifier grammar per CV-003 specification.

Author: ASIT (Aircraft Systems Information Transponder)
Document: AMPEL360-CV-003 v3.0
"""

from aerospacemodel.ampel360 import (
    ArtifactID,
    IDFormat,
    IDGenerator,
    parse_identifier,
    validate_identifier,
    create_pbs_id,
    create_wbs_id,
    parse_pbs,
    parse_wbs,
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def example_1_basic_identifier():
    """Example 1: Create a basic artifact identifier."""
    print_section("Example 1: Basic Artifact Identifier")
    
    # Create a requirement for cryogenic fuel system
    artifact_id = ArtifactID(
        msn="MSN001",
        ata_chapter="28",
        section="10",
        subject="00",
        lc_phase="LC02",
        artifact_type="REQ",
        sequence="001"
    )
    
    print("Created artifact identifier for:")
    print("  - MSN: MSN001 (AMPEL360 Q100)")
    print("  - ATA: 28-10-00 (Cryogenic Fuel Storage)")
    print("  - Phase: LC02 (System Requirements)")
    print("  - Type: REQ (System Requirement)")
    print()
    print("Formats:")
    print(f"  Compact:    {artifact_id.to_compact()}")
    print(f"  Hyphenated: {artifact_id.to_hyphenated()}")
    print(f"  URN:        {artifact_id.to_urn()}")
    print()
    print(f"Phase Type: {artifact_id.get_phase_type()}")
    print(f"SSOT Root:  {artifact_id.get_ssot_root()}")


def example_2_parsing():
    """Example 2: Parse existing identifiers."""
    print_section("Example 2: Parsing Existing Identifiers")
    
    test_ids = [
        "AMPEL360_Q100_MSN001_ATA28-10-00_LC02_REQ_001",
        "AMPEL360-Q100-MSN001-ATA71-11-00-LC04-DES-042",
        "urn:ampel360:q100:msn001:ata95-10-00:lc05:mdl:003",
    ]
    
    for identifier in test_ids:
        print(f"Parsing: {identifier}")
        artifact_id = parse_identifier(identifier)
        
        if artifact_id:
            print(f"  ✓ Valid identifier")
            print(f"    ATA: {artifact_id.ata_chapter}-{artifact_id.section}-{artifact_id.subject}")
            print(f"    Phase: {artifact_id.lc_phase}")
            print(f"    Type: {artifact_id.artifact_type}")
        else:
            print(f"  ✗ Invalid identifier")
        print()


def example_3_auto_sequencing():
    """Example 3: Auto-sequencing with IDGenerator."""
    print_section("Example 3: Auto-Sequencing")
    
    generator = IDGenerator()
    
    print("Generating requirements for ATA 28-10-00 (Cryogenic Storage):")
    print()
    
    for i in range(1, 4):
        artifact_id = generator.generate(
            msn="MSN001",
            ata_chapter="28",
            section="10",
            subject="00",
            lc_phase="LC02",
            artifact_type="REQ"
        )
        print(f"  {i}. {artifact_id}")
    
    print()
    print("Generating design documents (different type, resets sequence):")
    print()
    
    for i in range(1, 3):
        artifact_id = generator.generate(
            msn="MSN001",
            ata_chapter="28",
            section="10",
            subject="00",
            lc_phase="LC04",
            artifact_type="DES"
        )
        print(f"  {i}. {artifact_id}")


def example_4_pbs_wbs():
    """Example 4: PBS and WBS structures."""
    print_section("Example 4: PBS/WBS Structures")
    
    # Create PBS for cryogenic tank
    pbs_id = create_pbs_id(
        axis="T",
        subdomain="C2",
        ata_chapter="28",
        section="10",
        subject="00",
        item_name="CRYO_TANK_FWD"
    )
    
    print("Product Breakdown Structure (PBS):")
    print(f"  {pbs_id}")
    print()
    
    pbs = parse_pbs(pbs_id)
    print("  Properties:")
    print(f"    Domain: {pbs.axis} (Technologies)")
    print(f"    Sub-domain: {pbs.subdomain} (Cryogenic Cells)")
    print(f"    ATA Path: {pbs.get_ata_path()}")
    print(f"    Novel Technology: {pbs.is_novel_technology()} ⭐")
    print()
    
    # Create WBS for requirements phase
    wbs_id = create_wbs_id(lc_phase="LC02", hierarchy="1.2.3")
    
    print("Work Breakdown Structure (WBS):")
    print(f"  {wbs_id}")
    print()
    
    wbs = parse_wbs(wbs_id)
    print("  Properties:")
    print(f"    Phase Code: {wbs.phase_code}")
    print(f"    LC Phase: {wbs.get_lc_phase()}")
    print(f"    Level: {wbs.get_level()}")
    print(f"    Parent: {wbs.get_parent()}")


def example_5_validation():
    """Example 5: Validation."""
    print_section("Example 5: Identifier Validation")
    
    test_cases = [
        ("AMPEL360_Q100_MSN001_ATA28-10-00_LC02_REQ_001", True),
        ("AMPEL360_Q100_MSN001_ATA99-10-00_LC02_REQ_001", False),  # Invalid ATA
        ("AMPEL360_Q100_MSN01_ATA28-10-00_LC02_REQ_001", False),   # Invalid MSN
        ("urn:ampel360:q100:msn001:ata28-10-00:lc02:req:001", True),
    ]
    
    for identifier, expected_valid in test_cases:
        is_valid, error = validate_identifier(identifier)
        status = "✓" if is_valid == expected_valid else "✗"
        
        print(f"{status} {identifier[:50]}...")
        if is_valid:
            print(f"   Valid identifier")
        else:
            print(f"   Invalid: {error}")
        print()


def example_6_novel_technology():
    """Example 6: Novel Technology Subdomains."""
    print_section("Example 6: Novel Technology Subdomains")
    
    novel_tech_examples = [
        ("T", "C2", "28", "Cryogenic Cells (H₂ fuel)"),
        ("T", "I2", "95", "Intelligence (AI/ML models)"),
        ("T", "P", "71", "Propulsion (Fuel cells)"),
    ]
    
    print("Novel Technology Subdomains (⭐):")
    print("Require full LC01-LC14 lifecycle activation\n")
    
    for axis, subdomain, ata, description in novel_tech_examples:
        pbs_id = create_pbs_id(
            axis=axis,
            subdomain=subdomain,
            ata_chapter=ata,
            section="10",
            subject="00",
            item_name="EXAMPLE_ITEM"
        )
        
        pbs = parse_pbs(pbs_id)
        print(f"  • {subdomain}: {description}")
        print(f"    PBS: {pbs_id}")
        print(f"    ATA: {ata}")
        print()


def main():
    """Run all examples."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "AMPEL360 Q100 Identifier Grammar Examples" + " " * 16 + "║")
    print("║" + " " * 18 + "CV-003 Specification v3.0" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")
    
    example_1_basic_identifier()
    example_2_parsing()
    example_3_auto_sequencing()
    example_4_pbs_wbs()
    example_5_validation()
    example_6_novel_technology()
    
    print_section("Summary")
    print("✅ All examples completed successfully!")
    print()
    print("For more information:")
    print("  • Specification: docs/specifications/AMPEL360_CV_003_CONTROLLED_VOCABULARY.md")
    print("  • Module README: src/aerospacemodel/ampel360/README.md")
    print("  • Tests: tests/test_ampel360_*.py")
    print()


if __name__ == "__main__":
    main()
