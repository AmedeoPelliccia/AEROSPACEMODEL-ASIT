"""
Tests for O-ORGANIZATIONS subdomain structure.

Validates:
- O-ORGANIZATIONS subdomain split: A (Authoritative) and B (Business Enforcement)
- Subdomain mapping in 00_INDEX.md
- Subdomain documentation in README.md
- Subdomain directory existence and ATA chapter placement
- Lifecycle activation entries for O subdomains
- Top-level 00_INDEX.md subdomain table
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml


# Resolve repository root
REPO_ROOT = Path(__file__).resolve().parent.parent
OPT_IN = REPO_ROOT / "OPT-IN_FRAMEWORK"
O_ORGS = OPT_IN / "O-ORGANIZATIONS"
LC_ACTIVATION = REPO_ROOT / "lifecycle" / "T_SUBDOMAIN_LC_ACTIVATION.yaml"


# =============================================================================
# O-ORGANIZATIONS Subdomain Tests
# =============================================================================


class TestOOrganizationsSubdomains:
    """Tests for O-ORGANIZATIONS subdomain structure (A/B split)."""

    A_AUTHORITATIVE = ["ATA_00-GENERAL",
                       "ATA_04-AIRWORTHINESS_LIMITATIONS",
                       "ATA_05-TIME_LIMITS_MAINT_CHECKS"]

    B_BUSINESS_ENFORCEMENT = ["ATA_01-MAINTENANCE_POLICY",
                              "ATA_02-OPERATIONS_ORG",
                              "ATA_03-SUPPORT_INFORMATION"]

    def test_o_organizations_directory_exists(self):
        assert O_ORGS.is_dir()

    def test_index_exists(self):
        assert (O_ORGS / "00_INDEX.md").exists()

    def test_readme_exists(self):
        assert (O_ORGS / "README.md").exists()

    def test_a_subdomain_directory_exists(self):
        assert (O_ORGS / "A-AUTHORITATIVE").is_dir()

    def test_b_subdomain_directory_exists(self):
        assert (O_ORGS / "B-BUSINESS_ENFORCEMENT").is_dir()

    @pytest.fixture
    def index_text(self) -> str:
        return (O_ORGS / "00_INDEX.md").read_text(encoding="utf-8")

    @pytest.fixture
    def readme_text(self) -> str:
        return (O_ORGS / "README.md").read_text(encoding="utf-8")

    def test_index_has_subdomain_table(self, index_text: str):
        assert "Subdomain Structure" in index_text

    def test_index_has_authoritative(self, index_text: str):
        assert "Authoritative" in index_text

    def test_index_has_business_enforcement(self, index_text: str):
        assert "Business Enforcement" in index_text

    def test_index_a_code(self, index_text: str):
        assert "**A**" in index_text

    def test_index_b_code(self, index_text: str):
        assert "**B**" in index_text

    def test_readme_has_subdomain_structure(self, readme_text: str):
        assert "Subdomain Structure" in readme_text

    def test_readme_describes_authoritative(self, readme_text: str):
        assert "Authoritative" in readme_text
        assert "regulatory" in readme_text.lower()

    def test_readme_describes_business_enforcement(self, readme_text: str):
        assert "Business Enforcement" in readme_text
        assert "business" in readme_text.lower()

    @pytest.mark.parametrize("ata_dir", A_AUTHORITATIVE)
    def test_authoritative_directories_exist(self, ata_dir: str):
        assert (O_ORGS / "A-AUTHORITATIVE" / ata_dir).is_dir(), \
            f"{ata_dir} must exist in A-AUTHORITATIVE/"

    @pytest.mark.parametrize("ata_dir", B_BUSINESS_ENFORCEMENT)
    def test_business_enforcement_directories_exist(self, ata_dir: str):
        assert (O_ORGS / "B-BUSINESS_ENFORCEMENT" / ata_dir).is_dir(), \
            f"{ata_dir} must exist in B-BUSINESS_ENFORCEMENT/"

    def test_o_subdomain_ata_chapters_total_six(self):
        total = len(self.A_AUTHORITATIVE) + len(self.B_BUSINESS_ENFORCEMENT)
        assert total == 6

    def test_index_paths_reference_a_subdomain(self, index_text: str):
        assert "A-AUTHORITATIVE/" in index_text

    def test_index_paths_reference_b_subdomain(self, index_text: str):
        assert "B-BUSINESS_ENFORCEMENT/" in index_text


# =============================================================================
# Top-Level Index Tests
# =============================================================================


class TestTopLevelIndexOOrganizations:
    """Tests that top-level 00_INDEX.md contains O-ORGANIZATIONS subdomain table."""

    @pytest.fixture
    def index_text(self) -> str:
        return (OPT_IN / "00_INDEX.md").read_text(encoding="utf-8")

    def test_has_organization_subdomains_section(self, index_text: str):
        assert "Organization Subdomains (O-ORGANIZATIONS)" in index_text

    def test_org_a_code(self, index_text: str):
        assert "Authoritative" in index_text

    def test_org_b_code(self, index_text: str):
        assert "Business Enforcement" in index_text


# =============================================================================
# Lifecycle Activation Tests
# =============================================================================


class TestLifecycleActivationOOrganizations:
    """Tests that lifecycle activation YAML includes O-ORGANIZATIONS subdomain entries."""

    @pytest.fixture
    def lc_data(self) -> dict:
        assert LC_ACTIVATION.exists(), "T_SUBDOMAIN_LC_ACTIVATION.yaml must exist"
        return yaml.safe_load(LC_ACTIVATION.read_text(encoding="utf-8"))

    def test_o_authoritative_entry(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "O_AUTHORITATIVE" in sd
        assert sd["O_AUTHORITATIVE"]["title"] == "Authoritative (A)"

    def test_o_business_enforcement_entry(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "O_BUSINESS_ENFORCEMENT" in sd
        assert sd["O_BUSINESS_ENFORCEMENT"]["title"] == "Business Enforcement (B)"

    def test_o_subdomains_have_standard_profile(self, lc_data: dict):
        sd = lc_data["subdomains"]
        for key in ["O_AUTHORITATIVE", "O_BUSINESS_ENFORCEMENT"]:
            assert sd[key]["profile"] == "standard_profile", \
                f"{key} must use standard_profile"

    def test_optin_paths_contain_subdomain_dirs(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "A-AUTHORITATIVE" in sd["O_AUTHORITATIVE"]["optin_path"]
        assert "B-BUSINESS_ENFORCEMENT" in sd["O_BUSINESS_ENFORCEMENT"]["optin_path"]

    def test_o_authoritative_has_cross_links(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "cross_links" in sd["O_AUTHORITATIVE"], \
            "O_AUTHORITATIVE must have cross_links"
        links = sd["O_AUTHORITATIVE"]["cross_links"]
        targets = [lnk["target"] for lnk in links]
        assert "P_PRODUCT_DEFINITION" in targets
        assert "P_SERVICE_INSTRUCTION" in targets

    def test_o_business_enforcement_has_cross_links(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "cross_links" in sd["O_BUSINESS_ENFORCEMENT"], \
            "O_BUSINESS_ENFORCEMENT must have cross_links"
        links = sd["O_BUSINESS_ENFORCEMENT"]["cross_links"]
        targets = [lnk["target"] for lnk in links]
        assert "P_SERVICE_INSTRUCTION" in targets
        assert "I_MAINTENANCE_ENVIRONMENTS" in targets


# =============================================================================
# Cross-Link Content Tests
# =============================================================================


class TestOOrganizationsCrossLinks:
    """Tests that O-ORGANIZATIONS README contains cross-domain integration section."""

    @pytest.fixture
    def readme_text(self) -> str:
        return (O_ORGS / "README.md").read_text(encoding="utf-8")

    def test_readme_has_cross_domain_section(self, readme_text: str):
        assert "Cross-Domain Integration" in readme_text

    def test_readme_links_to_p_programs(self, readme_text: str):
        assert "P-PROGRAMS" in readme_text

    def test_readme_links_to_t_technologies(self, readme_text: str):
        assert "T-TECHNOLOGIES" in readme_text

    def test_readme_links_to_i_infrastructures(self, readme_text: str):
        assert "I-INFRASTRUCTURES" in readme_text

    def test_readme_links_to_n_neural_networks(self, readme_text: str):
        assert "N-NEURAL_NETWORKS" in readme_text

    def test_readme_related_docs_has_p_programs_link(self, readme_text: str):
        assert "../P-PROGRAMS/README.md" in readme_text

    def test_readme_related_docs_has_lc_activation_link(self, readme_text: str):
        assert "T_SUBDOMAIN_LC_ACTIVATION.yaml" in readme_text
