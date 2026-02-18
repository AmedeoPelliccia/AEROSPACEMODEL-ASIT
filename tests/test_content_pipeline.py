"""
Tests for S1000D AMM Content Pipeline.

Tests the complete content transformation workflow through all five stages:
1. INGEST & NORMALIZE
2. VALIDATE & ENRICH
3. TRANSFORM TO S1000D
4. ASSEMBLE DATA MODULES
5. PUBLISH & QA
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import yaml

from aerospacemodel.asigt.engine import (
    ArtifactType,
    ExecutionContext,
    SourceArtifact,
)
from aerospacemodel.asigt.pipeline import (
    AssembleStage,
    ContentPipeline,
    IngestNormalizeStage,
    PipelineConfig,
    PipelineStageConfig,
    PipelineStageType,
    PublishQAStage,
    TransformStage,
    ValidateEnrichStage,
    create_amm_pipeline,
    execute_pipeline,
)


class TestPipelineConfig:
    """Test pipeline configuration loading and validation."""
    
    def test_pipeline_config_creation(self):
        """Test creating pipeline configuration."""
        config = PipelineConfig(
            pipeline_id="TEST-001",
            name="Test Pipeline",
            description="Test pipeline description",
            version="1.0.0",
            publication_type="AMM"
        )
        
        assert config.pipeline_id == "TEST-001"
        assert config.name == "Test Pipeline"
        assert config.version == "1.0.0"
        assert config.publication_type == "AMM"
    
    def test_pipeline_config_from_yaml(self, tmp_path):
        """Test loading pipeline configuration from YAML."""
        # Create test YAML
        yaml_content = {
            "pipeline": {
                "metadata": {
                    "pipeline_id": "AMM-TEST-001",
                    "name": "Test AMM Pipeline",
                    "description": "Test pipeline",
                    "version": "1.0.0",
                    "publication_type": "AMM"
                },
                "stages": [
                    {
                        "stage": "initialization",
                        "name": "Initialization",
                        "description": "Initialize pipeline",
                        "order": 1
                    },
                    {
                        "stage": "transformation",
                        "name": "Transformation",
                        "description": "Transform to S1000D",
                        "order": 2
                    }
                ]
            }
        }
        
        yaml_path = tmp_path / "test_pipeline.yaml"
        with open(yaml_path, "w") as f:
            yaml.dump(yaml_content, f)
        
        config = PipelineConfig.from_yaml(yaml_path)
        
        assert config.pipeline_id == "AMM-TEST-001"
        assert config.name == "Test AMM Pipeline"
        assert len(config.stages) == 2
    
    def test_stage_name_mapping(self):
        """Test stage name to type mapping."""
        mapping = PipelineConfig._map_stage_name_to_type
        
        assert mapping("initialization") == PipelineStageType.INGEST_NORMALIZE
        assert mapping("source_loading") == PipelineStageType.INGEST_NORMALIZE
        assert mapping("transformation") == PipelineStageType.TRANSFORM
        assert mapping("validation") == PipelineStageType.VALIDATE_ENRICH
        assert mapping("publication_assembly") == PipelineStageType.ASSEMBLE
        assert mapping("rendering") == PipelineStageType.PUBLISH_QA


class TestIngestNormalizeStage:
    """Test Ingest & Normalize stage."""
    
    def test_stage_creation(self):
        """Test creating ingest/normalize stage."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.INGEST_NORMALIZE,
            name="Ingest & Normalize",
            description="Load and normalize sources"
        )
        
        stage = IngestNormalizeStage(config)
        assert stage.config == config
    
    def test_load_sources_empty_kdb(self, tmp_path):
        """Test loading sources from empty KDB."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.INGEST_NORMALIZE,
            name="Ingest",
            description="Test"
        )
        stage = IngestNormalizeStage(config)
        
        # Create empty KDB structure
        kdb_root = tmp_path / "KDB"
        kdb_root.mkdir()
        
        context = ExecutionContext(
            contract_id="TEST-001",
            contract_version="1.0",
            baseline_id="BL-001",
            authority_reference="TEST",
            invocation_timestamp=datetime.now(),
            kdb_root=kdb_root,
            idb_root=tmp_path / "IDB",
            output_path=tmp_path / "output",
            run_archive_path=tmp_path / "runs"
        )
        
        state = {}
        sources = stage._load_sources(context, state)
        
        assert isinstance(sources, list)
        assert len(sources) == 0
    
    def test_normalize_sources(self):
        """Test normalizing source artifacts."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.INGEST_NORMALIZE,
            name="Test",
            description="Test"
        )
        stage = IngestNormalizeStage(config)
        
        # Create test source
        source = SourceArtifact(
            id="TEST-001",
            path=Path("/tmp/test.yaml"),
            artifact_type=ArtifactType.REQUIREMENT,
            content={
                "ata_chapter": "28",
                "title": "Test Requirement",
                "description": "Test description"
            },
            hash_sha256="abc123"
        )
        
        normalized = stage._normalize_sources([source])
        
        assert len(normalized) == 1
        assert normalized[0]["id"] == "TEST-001"
        assert normalized[0]["type"] == "requirement"
        assert "metadata" in normalized[0]
        assert normalized[0]["metadata"]["ata_chapter"] == "28"
    
    def test_execute_stage(self, tmp_path):
        """Test executing ingest/normalize stage."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.INGEST_NORMALIZE,
            name="Ingest",
            description="Test"
        )
        stage = IngestNormalizeStage(config)
        
        context = ExecutionContext(
            contract_id="TEST-001",
            contract_version="1.0",
            baseline_id="BL-001",
            authority_reference="TEST",
            invocation_timestamp=datetime.now(),
            kdb_root=tmp_path / "KDB",
            idb_root=tmp_path / "IDB",
            output_path=tmp_path / "output",
            run_archive_path=tmp_path / "runs"
        )
        
        state = {}
        result = stage.execute(context, state)
        
        assert result.stage_name == "ingest_normalize"
        assert "sources" in state


class TestValidateEnrichStage:
    """Test Validate & Enrich stage."""
    
    def test_stage_creation(self):
        """Test creating validate/enrich stage."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.VALIDATE_ENRICH,
            name="Validate & Enrich",
            description="Validate and enrich content"
        )
        
        stage = ValidateEnrichStage(config)
        assert stage.config == config
    
    def test_apply_brex_rules(self):
        """Test applying BREX rules."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.VALIDATE_ENRICH,
            name="Test",
            description="Test"
        )
        stage = ValidateEnrichStage(config)
        
        # Test source with ATA chapter
        source_with_ata = {
            "id": "TEST-001",
            "metadata": {"ata_chapter": "28"}
        }
        
        issues = stage._apply_brex_rules([source_with_ata])
        assert len(issues) == 0
        
        # Test source without ATA chapter
        source_without_ata = {
            "id": "TEST-002",
            "metadata": {}
        }
        
        issues = stage._apply_brex_rules([source_without_ata])
        assert len(issues) > 0
        assert "ATA chapter" in issues[0]
    
    def test_enrich_content(self):
        """Test content enrichment."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.VALIDATE_ENRICH,
            name="Test",
            description="Test"
        )
        stage = ValidateEnrichStage(config)
        
        sources = [
            {"id": "TEST-001", "content": {}}
        ]
        
        enriched = stage._enrich_content(sources)
        
        assert len(enriched) == 1
        assert "enrichment" in enriched[0]
        assert "timestamp" in enriched[0]["enrichment"]
        assert "applicability" in enriched[0]["enrichment"]


class TestTransformStage:
    """Test Transform to S1000D stage."""
    
    def test_stage_creation(self):
        """Test creating transform stage."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.TRANSFORM,
            name="Transform",
            description="Transform to S1000D"
        )
        
        stage = TransformStage(config)
        assert stage.config == config
    
    def test_generate_dmc(self):
        """Test DMC generation."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.TRANSFORM,
            name="Test",
            description="Test"
        )
        stage = TransformStage(config)
        
        source = {
            "id": "TEST-001",
            "metadata": {"ata_chapter": "28"}
        }
        
        dmc = stage._generate_dmc(source)
        
        assert "28" in dmc
        assert "AERO" in dmc
    
    def test_determine_dm_type(self):
        """Test DM type determination."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.TRANSFORM,
            name="Test",
            description="Test"
        )
        stage = TransformStage(config)
        
        req_source = {"type": "requirement"}
        assert stage._determine_dm_type(req_source) == ArtifactType.DM_DESCRIPTIVE
        
        task_source = {"type": "task"}
        assert stage._determine_dm_type(task_source) == ArtifactType.DM_PROCEDURAL
        
        fault_source = {"type": "fault_data"}
        assert stage._determine_dm_type(fault_source) == ArtifactType.DM_FAULT_ISOLATION
    
    def test_transform_to_s1000d(self, tmp_path):
        """Test transformation to S1000D."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.TRANSFORM,
            name="Test",
            description="Test"
        )
        stage = TransformStage(config)
        
        sources = [
            {
                "id": "TEST-001",
                "type": "requirement",
                "metadata": {"ata_chapter": "28"},
                "content": {
                    "title": "Test Requirement",
                    "description": "Test description"
                }
            }
        ]
        
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        
        context = ExecutionContext(
            contract_id="TEST-001",
            contract_version="1.0",
            baseline_id="BL-001",
            authority_reference="TEST",
            invocation_timestamp=datetime.now(),
            kdb_root=tmp_path / "KDB",
            idb_root=tmp_path / "IDB",
            output_path=output_dir,
            run_archive_path=tmp_path / "runs"
        )
        
        data_modules = stage._transform_to_s1000d(sources, context)
        
        assert len(data_modules) == 1
        assert data_modules[0].dmc is not None
        assert data_modules[0].path.exists()


class TestAssembleStage:
    """Test Assemble Data Modules stage."""
    
    def test_stage_creation(self):
        """Test creating assemble stage."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.ASSEMBLE,
            name="Assemble",
            description="Assemble data modules"
        )
        
        stage = AssembleStage(config)
        assert stage.config == config
    
    def test_generate_pm(self, tmp_path):
        """Test Publication Module generation."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.ASSEMBLE,
            name="Test",
            description="Test"
        )
        stage = AssembleStage(config)
        
        from aerospacemodel.asigt.engine import OutputArtifact
        
        data_modules = [
            OutputArtifact(
                id="DM-001",
                path=tmp_path / "dm1.xml",
                artifact_type=ArtifactType.DM_DESCRIPTIVE,
                dmc="AERO-A-28-00-00-00A-040A-A"
            )
        ]
        
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        
        context = ExecutionContext(
            contract_id="TEST-001",
            contract_version="1.0",
            baseline_id="BL-001",
            authority_reference="TEST",
            invocation_timestamp=datetime.now(),
            kdb_root=tmp_path / "KDB",
            idb_root=tmp_path / "IDB",
            output_path=output_dir,
            run_archive_path=tmp_path / "runs"
        )
        
        pm = stage._generate_pm(data_modules, context)
        
        assert pm.artifact_type == ArtifactType.PM
        assert pm.path.exists()
    
    def test_generate_dml(self, tmp_path):
        """Test Data Module List generation."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.ASSEMBLE,
            name="Test",
            description="Test"
        )
        stage = AssembleStage(config)
        
        from aerospacemodel.asigt.engine import OutputArtifact
        
        data_modules = [
            OutputArtifact(
                id="DM-001",
                path=tmp_path / "dm1.xml",
                artifact_type=ArtifactType.DM_DESCRIPTIVE,
                dmc="AERO-A-28-00-00-00A-040A-A"
            )
        ]
        
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        
        context = ExecutionContext(
            contract_id="TEST-001",
            contract_version="1.0",
            baseline_id="BL-001",
            authority_reference="TEST",
            invocation_timestamp=datetime.now(),
            kdb_root=tmp_path / "KDB",
            idb_root=tmp_path / "IDB",
            output_path=output_dir,
            run_archive_path=tmp_path / "runs"
        )
        
        dml = stage._generate_dml(data_modules, context)
        
        assert dml.artifact_type == ArtifactType.DML
        assert dml.path.exists()


class TestPublishQAStage:
    """Test Publish & QA stage."""
    
    def test_stage_creation(self):
        """Test creating publish/QA stage."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.PUBLISH_QA,
            name="Publish & QA",
            description="Publish and perform QA"
        )
        
        stage = PublishQAStage(config)
        assert stage.config == config
    
    def test_perform_qa(self, tmp_path):
        """Test QA checks."""
        config = PipelineStageConfig(
            stage_type=PipelineStageType.PUBLISH_QA,
            name="Test",
            description="Test"
        )
        stage = PublishQAStage(config)
        
        from aerospacemodel.asigt.engine import OutputArtifact
        
        # Create test DM file
        dm_path = tmp_path / "dm1.xml"
        dm_path.write_text("<?xml version='1.0'?><dmodule/>")
        
        data_modules = [
            OutputArtifact(
                id="DM-001",
                path=dm_path,
                artifact_type=ArtifactType.DM_DESCRIPTIVE,
                dmc="AERO-A-28-00-00-00A-040A-A"
            )
        ]
        
        # Create PM
        pm_path = tmp_path / "pm.xml"
        pm_path.write_text("<?xml version='1.0'?><pm/>")
        
        pm = OutputArtifact(
            id="PM-001",
            path=pm_path,
            artifact_type=ArtifactType.PM
        )
        
        qa_results = stage._perform_qa(data_modules, pm)
        
        assert "total_checks" in qa_results
        assert "passed" in qa_results
        assert isinstance(qa_results["warnings"], list)


class TestContentPipeline:
    """Test complete Content Pipeline orchestration."""
    
    def test_pipeline_creation_from_config(self):
        """Test creating pipeline from configuration."""
        config = PipelineConfig(
            pipeline_id="TEST-001",
            name="Test Pipeline",
            description="Test",
            version="1.0.0",
            publication_type="AMM"
        )
        
        pipeline = ContentPipeline(config)
        
        assert pipeline.config == config
        assert pipeline.engine is not None
    
    def test_pipeline_validation(self):
        """Test pipeline configuration validation."""
        # Valid config
        config = PipelineConfig(
            pipeline_id="TEST-001",
            name="Test Pipeline",
            description="Test",
            version="1.0.0",
            publication_type="AMM"
        )
        config.stages.append(
            PipelineStageConfig(
                stage_type=PipelineStageType.INGEST_NORMALIZE,
                name="Test",
                description="Test"
            )
        )
        
        pipeline = ContentPipeline(config)
        is_valid, errors = pipeline.validate_config()
        
        assert is_valid
        assert len(errors) == 0
        
        # Invalid config (no stages)
        invalid_config = PipelineConfig(
            pipeline_id="TEST-002",
            name="Invalid Pipeline",
            description="Test",
            version="1.0.0",
            publication_type="AMM"
        )
        
        invalid_pipeline = ContentPipeline(invalid_config)
        is_valid, errors = invalid_pipeline.validate_config()
        
        assert not is_valid
        assert len(errors) > 0
    
    def test_pipeline_from_yaml(self, tmp_path):
        """Test creating pipeline from YAML file."""
        yaml_content = {
            "pipeline": {
                "metadata": {
                    "pipeline_id": "AMM-001",
                    "name": "AMM Pipeline",
                    "description": "Test AMM pipeline",
                    "version": "1.0.0",
                    "publication_type": "AMM"
                },
                "stages": [
                    {
                        "stage": "source_loading",
                        "name": "Load Sources",
                        "description": "Load source artifacts",
                        "order": 1
                    }
                ]
            }
        }
        
        yaml_path = tmp_path / "pipeline.yaml"
        with open(yaml_path, "w") as f:
            yaml.dump(yaml_content, f)
        
        pipeline = ContentPipeline.from_yaml(yaml_path)
        
        assert pipeline.config.pipeline_id == "AMM-001"
        assert pipeline.config.publication_type == "AMM"
    
    def test_convenience_function_create_amm_pipeline(self, tmp_path):
        """Test create_amm_pipeline convenience function."""
        yaml_content = {
            "pipeline": {
                "metadata": {
                    "pipeline_id": "AMM-001",
                    "name": "AMM Pipeline",
                    "description": "Test",
                    "version": "1.0.0",
                    "publication_type": "AMM"
                },
                "stages": []
            }
        }
        
        yaml_path = tmp_path / "amm.yaml"
        with open(yaml_path, "w") as f:
            yaml.dump(yaml_content, f)
        
        pipeline = create_amm_pipeline(yaml_path)
        
        assert isinstance(pipeline, ContentPipeline)
        assert pipeline.config.publication_type == "AMM"


class TestEndToEndPipeline:
    """End-to-end integration tests for the complete pipeline."""
    
    def test_complete_pipeline_execution(self, tmp_path):
        """Test executing complete pipeline end-to-end."""
        # Create test directories
        kdb_root = tmp_path / "KDB"
        kdb_root.mkdir()
        (kdb_root / "SSOT" / "requirements").mkdir(parents=True)
        
        # Create test requirement
        req_data = {
            "id": "REQ-001",
            "ata_chapter": "28",
            "title": "Fuel System Requirement",
            "description": "Test fuel system requirement"
        }
        
        req_file = kdb_root / "SSOT" / "requirements" / "REQ-001.yaml"
        with open(req_file, "w") as f:
            yaml.dump(req_data, f)
        
        # Create pipeline config
        pipeline_yaml = {
            "pipeline": {
                "metadata": {
                    "pipeline_id": "AMM-TEST-001",
                    "name": "Test AMM Pipeline",
                    "description": "End-to-end test pipeline",
                    "version": "1.0.0",
                    "publication_type": "AMM"
                },
                "stages": [
                    {
                        "stage": "source_loading",
                        "name": "Load Sources",
                        "description": "Load sources",
                        "order": 1
                    },
                    {
                        "stage": "transformation",
                        "name": "Transform",
                        "description": "Transform to S1000D",
                        "order": 2
                    }
                ]
            }
        }
        
        pipeline_path = tmp_path / "pipeline.yaml"
        with open(pipeline_path, "w") as f:
            yaml.dump(pipeline_yaml, f)
        
        # Create output directory
        output_path = tmp_path / "output"
        output_path.mkdir()
        
        # Execute pipeline using convenience function
        result = execute_pipeline(
            pipeline_yaml=pipeline_path,
            contract_id="TEST-CONTRACT-001",
            baseline_id="BL-001",
            kdb_root=kdb_root,
            output_path=output_path
        )
        
        # Verify result
        assert result is not None
        assert result.run_id is not None
        assert result.contract_id == "TEST-CONTRACT-001"


# =============================================================================
# TESTS – Inline regulatory-reference citations
# =============================================================================


class TestRegulatoryReferenceCitations:
    """Tests for preservation of regulatory references and best practices as
    inline citations in generated S1000D data modules (issue:
    'Preserve regulatory references and industry best practices as inline
    citations').
    """

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_stage_cfg(self, stage_type=PipelineStageType.TRANSFORM) -> PipelineStageConfig:
        return PipelineStageConfig(
            stage_type=stage_type,
            name="Test",
            description="Test stage",
        )

    def _transform_source(self, content: dict, tmp_path: Path) -> str:
        """Run TransformStage on a single source dict; return XML string."""
        from aerospacemodel.asigt.engine import ExecutionContext

        stage = TransformStage(self._make_stage_cfg())
        context = ExecutionContext(
            contract_id="TEST-CONTRACT",
            contract_version="1.0",
            baseline_id="BL-001",
            authority_reference="TEST",
            invocation_timestamp=datetime.now(),
            kdb_root=tmp_path,
            idb_root=tmp_path / "IDB",
            output_path=tmp_path / "output",
            run_archive_path=tmp_path / "runs",
        )
        state: dict = {
            "enriched_sources": [
                {
                    "id": "SRC-001",
                    "type": "requirement",
                    "metadata": {"ata_chapter": "28"},
                    "content": content,
                }
            ]
        }
        stage.execute(context, state)
        dm_files = list((tmp_path / "output").glob("*.xml"))
        assert dm_files, "No XML output produced by TransformStage"
        return dm_files[0].read_text(encoding="utf-8")

    # ------------------------------------------------------------------
    # TransformStage tests
    # ------------------------------------------------------------------

    def test_regulatory_refs_as_strings_appear_in_xml(self, tmp_path):
        """String regulatory refs appear as externalPubCode elements in XML."""
        xml = self._transform_source(
            {
                "title": "LH2 Tank General",
                "description": "Cryogenic hydrogen tank.",
                "regulatory_refs": ["EASA CS-25", "ARP4761", "DO-160"],
            },
            tmp_path,
        )
        assert "<externalPubCode>EASA CS-25</externalPubCode>" in xml
        assert "<externalPubCode>ARP4761</externalPubCode>" in xml
        assert "<externalPubCode>DO-160</externalPubCode>" in xml

    def test_regulatory_refs_as_dicts_include_title(self, tmp_path):
        """Dict regulatory refs preserve both code and title."""
        xml = self._transform_source(
            {
                "title": "Fuel System",
                "description": "Fuel system overview.",
                "regulatory_refs": [
                    {"standard": "DO-178C", "title": "Software Considerations in Airborne Systems"},
                ],
            },
            tmp_path,
        )
        assert "<externalPubCode>DO-178C</externalPubCode>" in xml
        assert "<externalPubTitle>Software Considerations in Airborne Systems</externalPubTitle>" in xml

    def test_best_practices_appear_in_xml(self, tmp_path):
        """Best-practice entries are emitted alongside regulatory refs."""
        xml = self._transform_source(
            {
                "title": "Maintenance Procedure",
                "description": "Step-by-step maintenance.",
                "best_practices": ["SAE ARP4754A"],
            },
            tmp_path,
        )
        assert "<externalPubCode>SAE ARP4754A</externalPubCode>" in xml

    def test_inline_citations_section_in_content(self, tmp_path):
        """The description block contains a levelled-para for inline citations."""
        xml = self._transform_source(
            {
                "title": "System Description",
                "description": "Overview.",
                "regulatory_refs": ["S1000D 5.0"],
                "best_practices": ["ARP4761"],
            },
            tmp_path,
        )
        assert "Regulatory References and Industry Best Practices" in xml
        assert "[S1000D 5.0]" in xml
        assert "[ARP4761]" in xml

    def test_no_refs_produces_no_citations_section(self, tmp_path):
        """No regulatory_refs → no citations section emitted."""
        xml = self._transform_source(
            {"title": "Basic DM", "description": "No refs here."},
            tmp_path,
        )
        assert "Regulatory References" not in xml
        assert "externalPubRef" not in xml

    def test_standards_field_alias(self, tmp_path):
        """The 'standards' field is treated as a supplement/alias for 'regulatory_refs'."""
        xml = self._transform_source(
            {
                "title": "Standards Check",
                "description": ".",
                "standards": ["ISO 14687-2"],
            },
            tmp_path,
        )
        assert "<externalPubCode>ISO 14687-2</externalPubCode>" in xml

    def test_both_regulatory_refs_and_standards_merged(self, tmp_path):
        """When both 'regulatory_refs' and 'standards' are present both are emitted."""
        xml = self._transform_source(
            {
                "title": "Merged Fields",
                "description": ".",
                "regulatory_refs": ["CS-25"],
                "standards": ["ISO 14687-2"],
            },
            tmp_path,
        )
        assert "<externalPubCode>CS-25</externalPubCode>" in xml
        assert "<externalPubCode>ISO 14687-2</externalPubCode>" in xml

    def test_empty_regulatory_refs_does_not_suppress_standards(self, tmp_path):
        """An explicit empty regulatory_refs list does not suppress the 'standards' field."""
        xml = self._transform_source(
            {
                "title": "Empty Reg Refs",
                "description": ".",
                "regulatory_refs": [],
                "standards": ["ARP4754A"],
            },
            tmp_path,
        )
        assert "<externalPubCode>ARP4754A</externalPubCode>" in xml

    def test_xml_special_characters_escaped_in_refs(self, tmp_path):
        """Ref entries containing XML special characters are properly escaped."""
        xml = self._transform_source(
            {
                "title": "Special Chars",
                "description": ".",
                "regulatory_refs": [
                    {"standard": "CS-25 Amendment 27", "title": "Applicability: <All> & More"},
                ],
            },
            tmp_path,
        )
        assert "<externalPubCode>CS-25 Amendment 27</externalPubCode>" in xml

    def test_empty_string_ref_skipped(self, tmp_path):
        """Ref entries that resolve to an empty code are silently skipped."""
        xml = self._transform_source(
            {
                "title": "Empty Ref",
                "description": ".",
                "regulatory_refs": ["", "ARP4761"],
            },
            tmp_path,
        )
        assert xml.count("<externalPubRef>") == 1
        assert "<externalPubCode>ARP4761</externalPubCode>" in xml

    def test_dict_ref_with_unknown_keys_skipped(self, tmp_path):
        """Dict entries without a recognisable code key are silently skipped."""
        xml = self._transform_source(
            {
                "title": "Unknown Keys",
                "description": ".",
                "regulatory_refs": [
                    {"revision": "C", "year": 2020},   # no standard/code/name key
                    "DO-178C",                          # valid entry
                ],
            },
            tmp_path,
        )
        assert xml.count("<externalPubRef>") == 1
        assert "<externalPubCode>DO-178C</externalPubCode>" in xml

    def test_non_string_non_dict_ref_skipped(self, tmp_path):
        """Non-string, non-dict entries in the refs list are silently skipped."""
        xml = self._transform_source(
            {
                "title": "Invalid Type Ref",
                "description": ".",
                "regulatory_refs": [42, None, "CS-25"],
            },
            tmp_path,
        )
        assert xml.count("<externalPubRef>") == 1
        assert "<externalPubCode>CS-25</externalPubCode>" in xml

    # ------------------------------------------------------------------
    # ValidateEnrichStage tests
    # ------------------------------------------------------------------

    def test_enrich_merges_regulatory_refs_and_standards(self):
        """_enrich_content merges 'regulatory_refs' and 'standards' into enrichment."""
        stage = ValidateEnrichStage(
            self._make_stage_cfg(PipelineStageType.VALIDATE_ENRICH)
        )
        sources = [
            {
                "id": "SRC-001",
                "type": "requirement",
                "content": {
                    "title": "T",
                    "regulatory_refs": ["EASA CS-25"],
                    "standards": ["ARP4761"],
                },
            }
        ]
        enriched = stage._enrich_content(sources)
        assert "EASA CS-25" in enriched[0]["enrichment"]["regulatory_refs"]
        assert "ARP4761" in enriched[0]["enrichment"]["regulatory_refs"]

    def test_enrich_preserves_best_practices(self):
        """_enrich_content forwards best_practices into the enrichment dict."""
        stage = ValidateEnrichStage(
            self._make_stage_cfg(PipelineStageType.VALIDATE_ENRICH)
        )
        sources = [
            {
                "id": "SRC-002",
                "type": "task",
                "content": {
                    "title": "T",
                    "best_practices": ["SAE ARP4754A"],
                },
            }
        ]
        enriched = stage._enrich_content(sources)
        assert enriched[0]["enrichment"]["best_practices"] == ["SAE ARP4754A"]

    def test_enrich_empty_refs_produces_empty_lists(self):
        """When no refs present the enrichment lists are empty (not absent)."""
        stage = ValidateEnrichStage(
            self._make_stage_cfg(PipelineStageType.VALIDATE_ENRICH)
        )
        sources = [{"id": "SRC-003", "type": "requirement", "content": {"title": "X"}}]
        enriched = stage._enrich_content(sources)
        assert enriched[0]["enrichment"]["regulatory_refs"] == []
        assert enriched[0]["enrichment"]["best_practices"] == []

    # ------------------------------------------------------------------
    # DescriptiveDMGenerator tests
    # ------------------------------------------------------------------

    def test_descriptive_generator_refs_in_dm_status(self, tmp_path):
        """DescriptiveDMGenerator emits refs in dmStatus for regulatory_refs."""
        from aerospacemodel.asigt.generators import (
            DescriptiveDMGenerator,
            GeneratorConfig,
        )
        from aerospacemodel.asigt.engine import ArtifactType, SourceArtifact

        config = GeneratorConfig(
            model_ident_code="AERO",
            organization_name="Test Org",
            organization_cage="00000",
        )
        gen = DescriptiveDMGenerator(config)

        src_path = tmp_path / "req.yaml"
        src_path.write_text("title: Fuel Tank\n")

        source = SourceArtifact(
            id="REQ-001",
            path=src_path,
            artifact_type=ArtifactType.REQUIREMENT,
            content={
                "title": "LH2 Tank",
                "ata_chapter": "28",
                "regulatory_refs": ["EASA CS-25", "ARP4761"],
                "best_practices": [
                    {"standard": "DO-160", "title": "Environmental Conditions"}
                ],
            },
        )

        result = gen.generate(source)

        assert result.success, f"Generator failed: {result.errors}"
        assert "<externalPubCode>EASA CS-25</externalPubCode>" in result.xml_content
        assert "<externalPubCode>ARP4761</externalPubCode>" in result.xml_content
        assert "<externalPubCode>DO-160</externalPubCode>" in result.xml_content
        assert "<externalPubTitle>Environmental Conditions</externalPubTitle>" in result.xml_content

    def test_descriptive_generator_inline_citations_in_content(self, tmp_path):
        """DescriptiveDMGenerator adds inline citations levelledPara to content."""
        from aerospacemodel.asigt.generators import (
            DescriptiveDMGenerator,
            GeneratorConfig,
        )
        from aerospacemodel.asigt.engine import ArtifactType, SourceArtifact

        config = GeneratorConfig(model_ident_code="AERO", organization_name="Test Org", organization_cage="00000")
        gen = DescriptiveDMGenerator(config)

        src_path = tmp_path / "req2.yaml"
        src_path.write_text("title: Test\n")

        source = SourceArtifact(
            id="REQ-002",
            path=src_path,
            artifact_type=ArtifactType.REQUIREMENT,
            content={
                "title": "System Overview",
                "ata_chapter": "28",
                "description": "Overview text.",
                "regulatory_refs": ["S1000D 5.0"],
            },
        )

        result = gen.generate(source)
        assert result.success
        assert "Regulatory References and Industry Best Practices" in result.xml_content
        assert "[S1000D 5.0]" in result.xml_content

    def test_descriptive_generator_no_refs_no_citations_section(self, tmp_path):
        """DescriptiveDMGenerator does not emit citations section when no refs."""
        from aerospacemodel.asigt.generators import (
            DescriptiveDMGenerator,
            GeneratorConfig,
        )
        from aerospacemodel.asigt.engine import ArtifactType, SourceArtifact

        config = GeneratorConfig(model_ident_code="AERO", organization_name="Test Org", organization_cage="00000")
        gen = DescriptiveDMGenerator(config)

        src_path = tmp_path / "req3.yaml"
        src_path.write_text("title: No refs\n")

        source = SourceArtifact(
            id="REQ-003",
            path=src_path,
            artifact_type=ArtifactType.REQUIREMENT,
            content={"title": "No Refs DM", "ata_chapter": "28"},
        )

        result = gen.generate(source)
        assert result.success
        assert "Regulatory References" not in result.xml_content
        assert "externalPubRef" not in result.xml_content

    # ------------------------------------------------------------------
    # ProceduralDMGenerator tests
    # ------------------------------------------------------------------

    def test_procedural_generator_refs_in_dm_status(self, tmp_path):
        """ProceduralDMGenerator emits refs in dmStatus for regulatory_refs."""
        from aerospacemodel.asigt.generators import (
            ProceduralDMGenerator,
            GeneratorConfig,
        )
        from aerospacemodel.asigt.engine import ArtifactType, SourceArtifact

        config = GeneratorConfig(model_ident_code="AERO", organization_name="Test Org", organization_cage="00000")
        gen = ProceduralDMGenerator(config)

        src_path = tmp_path / "task.yaml"
        src_path.write_text("title: Maintenance Task\n")

        source = SourceArtifact(
            id="TASK-001",
            path=src_path,
            artifact_type=ArtifactType.TASK,
            content={
                "task_title": "LH2 Tank Inspection",
                "task_type": "inspection",
                "ata_chapter": "28",
                "regulatory_refs": ["ARP4761"],
                "best_practices": ["ISO 14687-2"],
            },
        )

        result = gen.generate(source)
        assert result.success, f"Generator failed: {result.errors}"
        assert "<externalPubCode>ARP4761</externalPubCode>" in result.xml_content
        assert "<externalPubCode>ISO 14687-2</externalPubCode>" in result.xml_content
