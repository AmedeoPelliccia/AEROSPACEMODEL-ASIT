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
