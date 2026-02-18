"""
Tests for P-PROGRAMS, I-INFRASTRUCTURES, and N-NEURAL_NETWORKS subdomain structure.

Validates:
- P-PROGRAMS subdomain split: P (Product Definition) and S (Service Instruction)
- I-INFRASTRUCTURES subdomain split: M1 (Manufacturing), M2 (Maintenance), O (Operations)
- N-NEURAL_NETWORKS subdomain split: D (Digital Thread), A (AI Governance), P* (Reserved)
- Subdomain mapping in 00_INDEX.md files
- Subdomain documentation in README.md files
- AI Governance & Assurance directory existence
- Lifecycle activation entries for P/I/N subdomains
- Top-level 00_INDEX.md subdomain tables
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml


# Resolve repository root
REPO_ROOT = Path(__file__).resolve().parent.parent
OPT_IN = REPO_ROOT / "OPT-IN_FRAMEWORK"
P_PROGRAMS = OPT_IN / "P-PROGRAMS"
I_INFRA = OPT_IN / "I-INFRASTRUCTURES"
N_NEURAL = OPT_IN / "N-NEURAL_NETWORKS"
LC_ACTIVATION = REPO_ROOT / "lifecycle" / "T_SUBDOMAIN_LC_ACTIVATION.yaml"


# =============================================================================
# P-PROGRAMS Subdomain Tests
# =============================================================================


class TestPProgramsSubdomains:
    """Tests for P-PROGRAMS subdomain structure (P/S split)."""

    P_PRODUCT_DEFINITION = ["ATA_06-DIMENSIONS_AND_AREAS",
                            "ATA_08-LEVELING_AND_WEIGHING",
                            "ATA_11-PLACARDS_AND_MARKINGS"]

    S_SERVICE_INSTRUCTION = ["ATA_07-LIFTING_AND_SHORING",
                             "ATA_09-TOWING_AND_TAXIING",
                             "ATA_10-PARKING_MOORING_STORAGE_RETURN_TO_SERVICE",
                             "ATA_12-SERVICING"]

    def test_p_programs_directory_exists(self):
        assert P_PROGRAMS.is_dir()

    def test_index_exists(self):
        assert (P_PROGRAMS / "00_INDEX.md").exists()

    def test_readme_exists(self):
        assert (P_PROGRAMS / "README.md").exists()

    def test_p_subdomain_directory_exists(self):
        assert (P_PROGRAMS / "P-PRODUCT_DEFINITION").is_dir()

    def test_s_subdomain_directory_exists(self):
        assert (P_PROGRAMS / "S-SERVICE_INSTRUCTION").is_dir()

    @pytest.fixture
    def index_text(self) -> str:
        return (P_PROGRAMS / "00_INDEX.md").read_text(encoding="utf-8")

    @pytest.fixture
    def readme_text(self) -> str:
        return (P_PROGRAMS / "README.md").read_text(encoding="utf-8")

    def test_index_has_subdomain_table(self, index_text: str):
        assert "Subdomain Structure" in index_text

    def test_index_has_product_definition(self, index_text: str):
        assert "Product Definition" in index_text

    def test_index_has_service_instruction(self, index_text: str):
        assert "Service Instruction" in index_text

    def test_index_p_code(self, index_text: str):
        assert "**P**" in index_text

    def test_index_s_code(self, index_text: str):
        assert "**S**" in index_text

    def test_readme_has_subdomain_structure(self, readme_text: str):
        assert "Subdomain Structure" in readme_text

    def test_readme_describes_product_definition(self, readme_text: str):
        assert "Product Definition" in readme_text
        assert "What the product is" in readme_text

    def test_readme_describes_service_instruction(self, readme_text: str):
        assert "Service Instruction" in readme_text
        assert "How you handle it" in readme_text

    @pytest.mark.parametrize("ata_dir", P_PRODUCT_DEFINITION)
    def test_product_definition_directories_exist(self, ata_dir: str):
        assert (P_PROGRAMS / "P-PRODUCT_DEFINITION" / ata_dir).is_dir(), \
            f"{ata_dir} must exist in P-PRODUCT_DEFINITION/"

    @pytest.mark.parametrize("ata_dir", S_SERVICE_INSTRUCTION)
    def test_service_instruction_directories_exist(self, ata_dir: str):
        assert (P_PROGRAMS / "S-SERVICE_INSTRUCTION" / ata_dir).is_dir(), \
            f"{ata_dir} must exist in S-SERVICE_INSTRUCTION/"

    def test_p_subdomain_ata_chapters_total_seven(self):
        total = len(self.P_PRODUCT_DEFINITION) + len(self.S_SERVICE_INSTRUCTION)
        assert total == 7


# =============================================================================
# I-INFRASTRUCTURES Subdomain Tests
# =============================================================================


class TestIInfrastructuresSubdomains:
    """Tests for I-INFRASTRUCTURES subdomain structure (M1/M2/O split)."""

    M1_MANUFACTURING = ["ATA_85-FUEL_CELL_SYSTEMS_INFRA"]

    M2_MAINTENANCE = ["ATA_08-LEVELING_AND_WEIGHING_INFRA",
                      "ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA",
                      "ATA_12-SERVICING_INFRA"]

    O_OPERATIONS = ["ATA_03-SUPPORT_INFRA",
                    "ATA_IN_H2_GSE_AND_SUPPLY_CHAIN"]

    def test_i_infra_directory_exists(self):
        assert I_INFRA.is_dir()

    def test_index_exists(self):
        assert (I_INFRA / "00_INDEX.md").exists()

    def test_readme_exists(self):
        assert (I_INFRA / "README.md").exists()

    def test_m1_subdomain_directory_exists(self):
        assert (I_INFRA / "M1-MANUFACTURING_FACILITIES").is_dir()

    def test_m2_subdomain_directory_exists(self):
        assert (I_INFRA / "M2-MAINTENANCE_ENVIRONMENTS").is_dir()

    def test_o_subdomain_directory_exists(self):
        assert (I_INFRA / "O-OPERATIONS_SERVICE_STRUCTURES").is_dir()

    @pytest.fixture
    def index_text(self) -> str:
        return (I_INFRA / "00_INDEX.md").read_text(encoding="utf-8")

    @pytest.fixture
    def readme_text(self) -> str:
        return (I_INFRA / "README.md").read_text(encoding="utf-8")

    def test_index_has_subdomain_table(self, index_text: str):
        assert "Subdomain Structure" in index_text

    def test_index_has_m1_manufacturing(self, index_text: str):
        assert "Manufacturing Facilities" in index_text
        assert "**M1**" in index_text

    def test_index_has_m2_maintenance(self, index_text: str):
        assert "Maintenance Environments" in index_text
        assert "**M2**" in index_text

    def test_index_has_o_operations(self, index_text: str):
        assert "Operations & Service Structures" in index_text
        assert "**O**" in index_text

    def test_readme_has_subdomain_structure(self, readme_text: str):
        assert "Subdomain Structure" in readme_text

    def test_readme_describes_manufacturing(self, readme_text: str):
        assert "Manufacturing Facilities" in readme_text
        assert "Factory floor" in readme_text

    def test_readme_describes_maintenance(self, readme_text: str):
        assert "Maintenance Environments" in readme_text
        assert "Maintenance ecosystem" in readme_text

    def test_readme_describes_operations(self, readme_text: str):
        assert "Operations & Service Structures" in readme_text

    @pytest.mark.parametrize("cat_dir", M1_MANUFACTURING)
    def test_m1_directories_exist(self, cat_dir: str):
        assert (I_INFRA / "M1-MANUFACTURING_FACILITIES" / cat_dir).is_dir(), \
            f"{cat_dir} must exist in M1-MANUFACTURING_FACILITIES/"

    @pytest.mark.parametrize("cat_dir", M2_MAINTENANCE)
    def test_m2_directories_exist(self, cat_dir: str):
        assert (I_INFRA / "M2-MAINTENANCE_ENVIRONMENTS" / cat_dir).is_dir(), \
            f"{cat_dir} must exist in M2-MAINTENANCE_ENVIRONMENTS/"

    @pytest.mark.parametrize("cat_dir", O_OPERATIONS)
    def test_o_directories_exist(self, cat_dir: str):
        assert (I_INFRA / "O-OPERATIONS_SERVICE_STRUCTURES" / cat_dir).is_dir(), \
            f"{cat_dir} must exist in O-OPERATIONS_SERVICE_STRUCTURES/"

    def test_i_subdomain_categories_total_six(self):
        total = len(self.M1_MANUFACTURING) + len(self.M2_MAINTENANCE) + len(self.O_OPERATIONS)
        assert total == 6


# =============================================================================
# N-NEURAL_NETWORKS Subdomain Tests
# =============================================================================


class TestNNeuralNetworksSubdomains:
    """Tests for N-NEURAL_NETWORKS subdomain structure (D/A/P* split)."""

    def test_n_neural_directory_exists(self):
        assert N_NEURAL.is_dir()

    def test_index_exists(self):
        assert (N_NEURAL / "00_INDEX.md").exists()

    def test_readme_exists(self):
        assert (N_NEURAL / "README.md").exists()

    @pytest.fixture
    def index_text(self) -> str:
        return (N_NEURAL / "00_INDEX.md").read_text(encoding="utf-8")

    @pytest.fixture
    def readme_text(self) -> str:
        return (N_NEURAL / "README.md").read_text(encoding="utf-8")

    def test_index_has_subdomain_table(self, index_text: str):
        assert "Subdomain Structure" in index_text

    def test_index_has_d_digital_thread(self, index_text: str):
        assert "Digital Thread & Traceability" in index_text
        assert "**D**" in index_text

    def test_index_has_a_ai_governance(self, index_text: str):
        assert "AI Governance & Assurance" in index_text
        assert "**A**" in index_text

    def test_index_has_p_star_reserved(self, index_text: str):
        assert "Program Reserved" in index_text
        assert "**P***" in index_text

    def test_readme_has_subdomain_structure(self, readme_text: str):
        assert "Subdomain Structure" in readme_text

    def test_readme_describes_digital_thread(self, readme_text: str):
        assert "Digital Thread & Traceability" in readme_text
        assert "plumbing" in readme_text.lower()

    def test_readme_describes_ai_governance(self, readme_text: str):
        assert "AI Governance & Assurance" in readme_text
        assert "policy layer" in readme_text.lower()

    def test_readme_describes_program_reserved(self, readme_text: str):
        assert "Program Reserved" in readme_text
        assert "Expansion slot" in readme_text

    def test_d_subdomain_directory_exists(self):
        assert (N_NEURAL / "D-DIGITAL_THREAD_TRACEABILITY").is_dir()

    def test_a_subdomain_directory_exists(self):
        assert (N_NEURAL / "A-AI_GOVERNANCE_ASSURANCE").is_dir()

    def test_pstar_subdomain_directory_exists(self):
        assert (N_NEURAL / "PSTAR-PROGRAM_RESERVED").is_dir()

    def test_ata96_directory_exists(self):
        assert (N_NEURAL / "D-DIGITAL_THREAD_TRACEABILITY" / "ATA_96-TRACEABILITY_DPP_LEDGER").is_dir()

    def test_ata98_directory_exists(self):
        assert (N_NEURAL / "PSTAR-PROGRAM_RESERVED" / "ATA_98-RESERVED_PROGRAM_SLOT").is_dir()

    def test_ai_governance_directory_exists(self):
        assert (N_NEURAL / "A-AI_GOVERNANCE_ASSURANCE" / "ATA_AI_GOVERNANCE_ASSURANCE").is_dir(), \
            "ATA_AI_GOVERNANCE_ASSURANCE/ directory must exist in A-AI_GOVERNANCE_ASSURANCE/"

    def test_readme_ai_governance_content(self, readme_text: str):
        assert "certification pathway" in readme_text.lower()
        assert "ethics" in readme_text.lower()
        assert "human authority" in readme_text.lower()
        assert "explainability" in readme_text.lower()


# =============================================================================
# Top-Level Index Subdomain Table Tests
# =============================================================================


class TestTopLevelIndexSubdomains:
    """Tests that OPT-IN_FRAMEWORK/00_INDEX.md contains P/I/N subdomain tables."""

    @pytest.fixture
    def index_text(self) -> str:
        return (OPT_IN / "00_INDEX.md").read_text(encoding="utf-8")

    def test_has_program_subdomains_section(self, index_text: str):
        assert "Program Subdomains (P-PROGRAMS)" in index_text

    def test_has_infrastructure_subdomains_section(self, index_text: str):
        assert "Infrastructure Subdomains (I-INFRASTRUCTURES)" in index_text

    def test_has_neural_network_subdomains_section(self, index_text: str):
        assert "Neural Network Subdomains (N-NEURAL_NETWORKS)" in index_text

    def test_program_p_code(self, index_text: str):
        assert "Product Definition" in index_text

    def test_program_s_code(self, index_text: str):
        assert "Service Instruction" in index_text

    def test_infra_m1_code(self, index_text: str):
        assert "Manufacturing Facilities" in index_text

    def test_infra_m2_code(self, index_text: str):
        assert "Maintenance Environments" in index_text

    def test_infra_o_code(self, index_text: str):
        assert "Operations & Service Structures" in index_text

    def test_neural_d_code(self, index_text: str):
        assert "Digital Thread & Traceability" in index_text

    def test_neural_a_code(self, index_text: str):
        assert "AI Governance & Assurance" in index_text

    def test_neural_p_star_code(self, index_text: str):
        assert "Program Reserved" in index_text


# =============================================================================
# Lifecycle Activation Tests
# =============================================================================


class TestLifecycleActivationSubdomains:
    """Tests that lifecycle activation YAML includes P/I/N subdomain entries."""

    @pytest.fixture
    def lc_data(self) -> dict:
        assert LC_ACTIVATION.exists(), "T_SUBDOMAIN_LC_ACTIVATION.yaml must exist"
        return yaml.safe_load(LC_ACTIVATION.read_text(encoding="utf-8"))

    def test_p_product_definition_entry(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "P_PRODUCT_DEFINITION" in sd
        assert sd["P_PRODUCT_DEFINITION"]["title"] == "Product Definition (P)"

    def test_p_service_instruction_entry(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "P_SERVICE_INSTRUCTION" in sd
        assert sd["P_SERVICE_INSTRUCTION"]["title"] == "Service Instruction (S)"

    def test_i_manufacturing_entry(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "I_MANUFACTURING_FACILITIES" in sd
        assert sd["I_MANUFACTURING_FACILITIES"]["title"] == "Manufacturing Facilities (M1)"

    def test_i_maintenance_entry(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "I_MAINTENANCE_ENVIRONMENTS" in sd
        assert sd["I_MAINTENANCE_ENVIRONMENTS"]["title"] == "Maintenance Environments (M2)"

    def test_i_operations_entry(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "I_OPERATIONS_SERVICE_STRUCTURES" in sd
        assert sd["I_OPERATIONS_SERVICE_STRUCTURES"]["title"] == "Operations & Service Structures (O)"

    def test_n_digital_thread_entry(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "N_DIGITAL_THREAD_TRACEABILITY" in sd
        assert sd["N_DIGITAL_THREAD_TRACEABILITY"]["title"] == "Digital Thread & Traceability (D)"

    def test_n_ai_governance_entry(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "N_AI_GOVERNANCE_ASSURANCE" in sd
        assert sd["N_AI_GOVERNANCE_ASSURANCE"]["title"] == "AI Governance & Assurance (A)"

    def test_n_program_reserved_entry(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "N_PROGRAM_RESERVED" in sd
        assert sd["N_PROGRAM_RESERVED"]["title"] == "Program Reserved (P*)"

    def test_all_pin_subdomains_have_standard_profile(self, lc_data: dict):
        sd = lc_data["subdomains"]
        pin_keys = [
            "P_PRODUCT_DEFINITION", "P_SERVICE_INSTRUCTION",
            "I_MANUFACTURING_FACILITIES", "I_MAINTENANCE_ENVIRONMENTS",
            "I_OPERATIONS_SERVICE_STRUCTURES",
            "N_DIGITAL_THREAD_TRACEABILITY", "N_AI_GOVERNANCE_ASSURANCE",
            "N_PROGRAM_RESERVED",
        ]
        for key in pin_keys:
            assert sd[key]["profile"] == "standard_profile", \
                f"{key} must use standard_profile"

    def test_optin_paths_contain_subdomain_dirs(self, lc_data: dict):
        sd = lc_data["subdomains"]
        expected = {
            "P_PRODUCT_DEFINITION": "P-PRODUCT_DEFINITION",
            "P_SERVICE_INSTRUCTION": "S-SERVICE_INSTRUCTION",
            "I_MANUFACTURING_FACILITIES": "M1-MANUFACTURING_FACILITIES",
            "I_MAINTENANCE_ENVIRONMENTS": "M2-MAINTENANCE_ENVIRONMENTS",
            "I_OPERATIONS_SERVICE_STRUCTURES": "O-OPERATIONS_SERVICE_STRUCTURES",
            "N_DIGITAL_THREAD_TRACEABILITY": "D-DIGITAL_THREAD_TRACEABILITY",
            "N_AI_GOVERNANCE_ASSURANCE": "A-AI_GOVERNANCE_ASSURANCE",
            "N_PROGRAM_RESERVED": "PSTAR-PROGRAM_RESERVED",
        }
        for key, subdir in expected.items():
            assert subdir in sd[key]["optin_path"], \
                f"{key} optin_path must contain {subdir}"

    def test_p_product_definition_has_cross_links(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "cross_links" in sd["P_PRODUCT_DEFINITION"], \
            "P_PRODUCT_DEFINITION must have cross_links"
        links = sd["P_PRODUCT_DEFINITION"]["cross_links"]
        targets = [lnk["target"] for lnk in links]
        assert "O_AUTHORITATIVE" in targets
        assert "N_DIGITAL_THREAD_TRACEABILITY" in targets

    def test_p_service_instruction_has_cross_links(self, lc_data: dict):
        sd = lc_data["subdomains"]
        assert "cross_links" in sd["P_SERVICE_INSTRUCTION"], \
            "P_SERVICE_INSTRUCTION must have cross_links"
        links = sd["P_SERVICE_INSTRUCTION"]["cross_links"]
        targets = [lnk["target"] for lnk in links]
        assert "O_BUSINESS_ENFORCEMENT" in targets
        assert "I_MAINTENANCE_ENVIRONMENTS" in targets


# =============================================================================
# P-PROGRAMS Cross-Link Content Tests
# =============================================================================


class TestPProgramsCrossLinks:
    """Tests that P-PROGRAMS README contains cross-domain integration section."""

    @pytest.fixture
    def readme_text(self) -> str:
        return (P_PROGRAMS / "README.md").read_text(encoding="utf-8")

    def test_readme_has_cross_domain_section(self, readme_text: str):
        assert "Cross-Domain Integration" in readme_text

    def test_readme_links_to_o_organizations(self, readme_text: str):
        assert "O-ORGANIZATIONS" in readme_text

    def test_readme_links_to_t_technologies(self, readme_text: str):
        assert "T-TECHNOLOGIES" in readme_text

    def test_readme_links_to_i_infrastructures(self, readme_text: str):
        assert "I-INFRASTRUCTURES" in readme_text

    def test_readme_links_to_n_neural_networks(self, readme_text: str):
        assert "N-NEURAL_NETWORKS" in readme_text

    def test_readme_related_docs_has_o_organizations_link(self, readme_text: str):
        assert "../O-ORGANIZATIONS/README.md" in readme_text

    def test_readme_related_docs_has_lc_activation_link(self, readme_text: str):
        assert "T_SUBDOMAIN_LC_ACTIVATION.yaml" in readme_text
