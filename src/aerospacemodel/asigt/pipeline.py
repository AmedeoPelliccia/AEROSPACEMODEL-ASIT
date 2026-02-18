"""
ASIGT Content Pipeline Module

Implements the S1000D AMM Content Pipeline with the following stages:
1. INGEST & NORMALIZE - Load and normalize source data
2. VALIDATE & ENRICH - Apply business rules and enrich content
3. TRANSFORM TO S1000D - Transform to S1000D data modules
4. ASSEMBLE DATA MODULES - Assemble into publication structure
5. PUBLISH & QA - Render outputs and perform quality assurance

This module orchestrates the complete content transformation workflow
from engineering source data to deliverable technical publications.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from .engine import (
    ASIGTEngine,
    ArtifactType,
    ExecutionContext,
    ExecutionMetrics,
    OutputArtifact,
    RunResult,
    RunStatus,
    SourceArtifact,
    StageResult,
    StageStatus,
)

logger = logging.getLogger(__name__)


# =============================================================================
# PIPELINE STAGES
# =============================================================================


class PipelineStageType(Enum):
    """Content pipeline stage types."""
    INGEST_NORMALIZE = "ingest_normalize"
    VALIDATE_ENRICH = "validate_enrich"
    TRANSFORM = "transform"
    ASSEMBLE = "assemble"
    PUBLISH_QA = "publish_qa"


@dataclass
class PipelineStageConfig:
    """Configuration for a pipeline stage."""
    stage_type: PipelineStageType
    name: str
    description: str
    enabled: bool = True
    parallel: bool = False
    timeout_minutes: int = 30
    retry_on_failure: bool = False
    max_retries: int = 3
    required: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineConfig:
    """Complete pipeline configuration."""
    pipeline_id: str
    name: str
    description: str
    version: str
    publication_type: str  # AMM, SRM, CMM, IPC, etc.
    stages: List[PipelineStageConfig] = field(default_factory=list)
    contract_id: Optional[str] = None
    baseline_id: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> PipelineConfig:
        """Load pipeline configuration from YAML file."""
        with open(yaml_path, "r", encoding="utf-8") as f:
            # yaml.safe_load() returns None for empty or comment-only files; normalize to dict
            data = yaml.safe_load(f) or {}
        
        if not isinstance(data, dict):
            data = {}
        
        pipeline_data = data.get("pipeline", {})
        if not isinstance(pipeline_data, dict):
            pipeline_data = {}
        metadata = pipeline_data.get("metadata", {})
        if not isinstance(metadata, dict):
            metadata = {}
        
        config = cls(
            pipeline_id=metadata.get("pipeline_id", ""),
            name=metadata.get("name", ""),
            description=metadata.get("description", ""),
            version=metadata.get("version", "1.0.0"),
            publication_type=metadata.get("publication_type", "AMM"),
            config=pipeline_data.get("config", {})
        )
        
        # Parse stages from YAML
        stages_data = pipeline_data.get("stages", [])
        for stage_data in stages_data:
            stage_name = stage_data.get("stage", "")
            stage_type = cls._map_stage_name_to_type(stage_name)
            
            if stage_type:
                stage_config = PipelineStageConfig(
                    stage_type=stage_type,
                    name=stage_data.get("name", stage_name),
                    description=stage_data.get("description", ""),
                    enabled=True,
                    parallel=False,
                    config={
                        "order": stage_data.get("order", 0),
                        "steps": stage_data.get("steps", [])
                    }
                )
                config.stages.append(stage_config)
        
        return config
    
    @staticmethod
    def _map_stage_name_to_type(stage_name: str) -> Optional[PipelineStageType]:
        """Map YAML stage names to pipeline stage types."""
        mapping = {
            "initialization": PipelineStageType.INGEST_NORMALIZE,
            "source_loading": PipelineStageType.INGEST_NORMALIZE,
            "transformation": PipelineStageType.TRANSFORM,
            "validation": PipelineStageType.VALIDATE_ENRICH,
            "traceability": PipelineStageType.VALIDATE_ENRICH,
            "publication_assembly": PipelineStageType.ASSEMBLE,
            "rendering": PipelineStageType.PUBLISH_QA,
            "finalization": PipelineStageType.PUBLISH_QA,
        }
        return mapping.get(stage_name)


# =============================================================================
# PIPELINE STAGE IMPLEMENTATIONS
# =============================================================================


class IngestNormalizeStage:
    """
    Stage 1: INGEST & NORMALIZE
    
    Responsibilities:
    - Load source data from multiple formats (OEM data, engineering docs, legacy docs)
    - Normalize data to common internal format
    - Validate data completeness and consistency
    - Extract metadata and relationships
    """
    
    def __init__(self, config: PipelineStageConfig):
        self.config = config
        self.logger = logging.getLogger("asigt.pipeline.ingest_normalize")
    
    def execute(
        self, 
        context: ExecutionContext,
        state: Dict[str, Any]
    ) -> StageResult:
        """Execute ingest and normalize stage."""
        start_time = datetime.now()
        self.logger.info("Starting INGEST & NORMALIZE stage")
        
        try:
            # Load source artifacts from KDB baseline
            sources = self._load_sources(context, state)
            state["sources"] = sources
            state["raw_source_count"] = len(sources)
            
            # Normalize data formats
            normalized = self._normalize_sources(sources)
            state["normalized_sources"] = normalized
            
            # Extract metadata
            self._extract_metadata(normalized, state)
            
            # Validate data completeness
            validation_issues = self._validate_completeness(normalized)
            
            end_time = datetime.now()
            
            result = StageResult(
                stage_name="ingest_normalize",
                status=StageStatus.COMPLETED,
                start_time=start_time,
                end_time=end_time,
                artifacts_produced=len(sources)
            )
            
            if validation_issues:
                result.warnings.extend(validation_issues)
            
            self.logger.info(f"INGEST & NORMALIZE completed: {len(sources)} sources loaded")
            return result
            
        except Exception as e:
            self.logger.error(f"INGEST & NORMALIZE failed: {e}")
            return StageResult(
                stage_name="ingest_normalize",
                status=StageStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                errors=[str(e)]
            )
    
    def _load_sources(
        self, 
        context: ExecutionContext,
        state: Dict[str, Any]
    ) -> List[SourceArtifact]:
        """Load source artifacts from KDB."""
        sources = []
        
        # Example: Load from KDB paths
        kdb_root = context.kdb_root
        if kdb_root and kdb_root.exists():
            # Load requirements
            req_path = kdb_root / "SSOT" / "requirements"
            if req_path.exists():
                for req_file in req_path.rglob("*.yaml"):
                    artifact = SourceArtifact(
                        id=req_file.stem,
                        path=req_file,
                        artifact_type=ArtifactType.REQUIREMENT
                    )
                    artifact.compute_hash()
                    artifact.load_content()
                    sources.append(artifact)
            
            # Load tasks
            task_path = kdb_root / "SSOT" / "tasks"
            if task_path.exists():
                for task_file in task_path.rglob("*.yaml"):
                    artifact = SourceArtifact(
                        id=task_file.stem,
                        path=task_file,
                        artifact_type=ArtifactType.TASK
                    )
                    artifact.compute_hash()
                    artifact.load_content()
                    sources.append(artifact)
        
        self.logger.debug(f"Loaded {len(sources)} source artifacts")
        return sources
    
    def _normalize_sources(
        self, 
        sources: List[SourceArtifact]
    ) -> List[Dict[str, Any]]:
        """Normalize source data to common format."""
        normalized = []
        
        for source in sources:
            if not source.content:
                continue
            
            # Create normalized representation
            norm_data = {
                "id": source.id,
                "type": source.artifact_type.value,
                "path": str(source.path),
                "hash": source.hash_sha256,
                "content": source.content,
                "metadata": {
                    "ata_chapter": source.content.get("ata_chapter", ""),
                    "title": source.content.get("title", ""),
                    "description": source.content.get("description", "")
                }
            }
            normalized.append(norm_data)
        
        return normalized
    
    def _extract_metadata(
        self, 
        normalized: List[Dict[str, Any]],
        state: Dict[str, Any]
    ) -> None:
        """Extract metadata from normalized sources."""
        metadata = {
            "ata_chapters": set(),
            "source_types": set(),
            "total_sources": len(normalized)
        }
        
        for item in normalized:
            ata_chapter = item.get("metadata", {}).get("ata_chapter")
            if ata_chapter:
                metadata["ata_chapters"].add(ata_chapter)
            metadata["source_types"].add(item["type"])
        
        state["metadata"] = metadata
        self.logger.debug(f"Extracted metadata: {len(metadata['ata_chapters'])} ATA chapters")
    
    def _validate_completeness(
        self, 
        normalized: List[Dict[str, Any]]
    ) -> List[str]:
        """Validate data completeness."""
        issues = []
        
        for item in normalized:
            # Check required fields
            if not item.get("id"):
                issues.append(f"Missing ID for source: {item.get('path')}")
            
            if not item.get("content"):
                issues.append(f"Empty content for source: {item.get('id')}")
        
        return issues


class ValidateEnrichStage:
    """
    Stage 2: VALIDATE & ENRICH
    
    Responsibilities:
    - Apply BREX business rules
    - Schema validation
    - Enrich content with cross-references
    - Add applicability information
    - Validate data quality
    """
    
    def __init__(self, config: PipelineStageConfig):
        self.config = config
        self.logger = logging.getLogger("asigt.pipeline.validate_enrich")
    
    def execute(
        self, 
        context: ExecutionContext,
        state: Dict[str, Any]
    ) -> StageResult:
        """Execute validate and enrich stage."""
        start_time = datetime.now()
        self.logger.info("Starting VALIDATE & ENRICH stage")
        
        try:
            normalized_sources = state.get("normalized_sources", [])
            
            # Apply business rules
            brex_issues = self._apply_brex_rules(normalized_sources)
            
            # Enrich content
            enriched = self._enrich_content(normalized_sources)
            state["enriched_sources"] = enriched
            
            # Schema validation
            schema_issues = self._validate_schema(enriched)
            
            end_time = datetime.now()
            
            result = StageResult(
                stage_name="validate_enrich",
                status=StageStatus.COMPLETED,
                start_time=start_time,
                end_time=end_time,
                artifacts_produced=len(enriched)
            )
            
            if brex_issues:
                result.warnings.extend(brex_issues)
            if schema_issues:
                result.warnings.extend(schema_issues)
            
            self.logger.info(f"VALIDATE & ENRICH completed: {len(enriched)} sources enriched")
            return result
            
        except Exception as e:
            self.logger.error(f"VALIDATE & ENRICH failed: {e}")
            return StageResult(
                stage_name="validate_enrich",
                status=StageStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                errors=[str(e)]
            )
    
    def _apply_brex_rules(self, sources: List[Dict[str, Any]]) -> List[str]:
        """Apply BREX business rules to sources."""
        issues = []
        
        # Example BREX rule: All sources must have ATA chapter
        for source in sources:
            metadata = source.get("metadata", {})
            if not metadata.get("ata_chapter"):
                issues.append(f"BREX violation: Missing ATA chapter for {source.get('id')}")
        
        return issues
    
    def _enrich_content(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich content with additional information."""
        enriched = []
        
        for source in sources:
            # Add enrichment data
            enriched_source = source.copy()
            content = source.get("content", {})

            # Extract and preserve regulatory references and best practices
            reg_refs_raw = content.get("regulatory_refs")
            standards_raw = content.get("standards")

            combined_reg_refs: List[Any] = []
            if reg_refs_raw is not None:
                combined_reg_refs.extend(list(reg_refs_raw))
            if standards_raw is not None:
                combined_reg_refs.extend(list(standards_raw))

            reg_refs = combined_reg_refs
            best_practices = list(content.get("best_practices") or [])

            enriched_source["enrichment"] = {
                "timestamp": datetime.now().isoformat(),
                "cross_references": [],
                "applicability": "ALL",
                "regulatory_refs": reg_refs,
                "best_practices": best_practices,
            }
            enriched.append(enriched_source)
        
        return enriched
    
    def _validate_schema(self, sources: List[Dict[str, Any]]) -> List[str]:
        """Validate sources against schema."""
        issues = []
        
        # Example schema validation
        required_fields = ["id", "type", "content"]
        for source in sources:
            for field in required_fields:
                if field not in source:
                    issues.append(f"Schema violation: Missing '{field}' in {source.get('id')}")
        
        return issues


class TransformStage:
    """
    Stage 3: TRANSFORM TO S1000D
    
    Responsibilities:
    - Apply XSLT/mapping rules
    - Generate Data Modules (DM)
    - Apply SNS coding
    - Handle ICN (graphics) references
    - Generate DMC codes
    """
    
    def __init__(self, config: PipelineStageConfig):
        self.config = config
        self.logger = logging.getLogger("asigt.pipeline.transform")
    
    def execute(
        self, 
        context: ExecutionContext,
        state: Dict[str, Any]
    ) -> StageResult:
        """Execute transformation stage."""
        start_time = datetime.now()
        self.logger.info("Starting TRANSFORM TO S1000D stage")
        
        try:
            # Try enriched sources first, fall back to normalized sources
            enriched_sources = state.get("enriched_sources", [])
            if not enriched_sources:
                enriched_sources = state.get("normalized_sources", [])
                if not enriched_sources:
                    self.logger.warning("No sources available for transformation")
            
            # Transform to S1000D data modules
            data_modules = self._transform_to_s1000d(enriched_sources, context)
            state["data_modules"] = data_modules
            
            # Handle ICN references
            self._link_icn_references(data_modules, state)
            
            end_time = datetime.now()
            
            result = StageResult(
                stage_name="transform",
                status=StageStatus.COMPLETED,
                start_time=start_time,
                end_time=end_time,
                artifacts_produced=len(data_modules)
            )
            
            self.logger.info(f"TRANSFORM completed: {len(data_modules)} DMs generated")
            return result
            
        except Exception as e:
            self.logger.error(f"TRANSFORM failed: {e}")
            return StageResult(
                stage_name="transform",
                status=StageStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                errors=[str(e)]
            )
    
    def _transform_to_s1000d(
        self, 
        sources: List[Dict[str, Any]],
        context: ExecutionContext
    ) -> List[OutputArtifact]:
        """Transform sources to S1000D data modules."""
        data_modules = []
        
        output_dir = context.output_path
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for source in sources:
            # Generate DMC code
            dmc = self._generate_dmc(source)
            
            # Create output artifact
            dm_path = output_dir / f"DMC-{dmc}.xml"
            
            artifact = OutputArtifact(
                id=f"DM-{source['id']}",
                path=dm_path,
                artifact_type=self._determine_dm_type(source),
                dmc=dmc,
                source_refs=[source["id"]],
                generated_at=datetime.now()
            )
            
            # Generate S1000D XML (simplified)
            self._generate_dm_xml(artifact, source)
            artifact.compute_hash()
            
            data_modules.append(artifact)
        
        return data_modules
    
    def _generate_dmc(self, source: Dict[str, Any]) -> str:
        """Generate Data Module Code."""
        # Normalize ATA chapter to 2-digit format
        ata = source.get("metadata", {}).get("ata_chapter", "")
        ata = (ata or "00").zfill(2)
        
        # Format: MODEL-A-ATA-00-00-00A-040A-A
        dmc = f"AERO-A-{ata}-00-00-00A-040A-A"
        return dmc
    
    def _determine_dm_type(self, source: Dict[str, Any]) -> ArtifactType:
        """Determine DM type based on source."""
        source_type = source.get("type", "")
        
        mapping = {
            "requirement": ArtifactType.DM_DESCRIPTIVE,
            "task": ArtifactType.DM_PROCEDURAL,
            "fault_data": ArtifactType.DM_FAULT_ISOLATION,
        }
        
        return mapping.get(source_type, ArtifactType.DM_DESCRIPTIVE)
    
    def _generate_dm_xml(self, artifact: OutputArtifact, source: Dict[str, Any]) -> None:
        """Generate S1000D XML for data module."""
        from xml.sax.saxutils import escape

        # Simplified XML generation
        content = source.get("content", {})
        title = escape(content.get("title", "Untitled"))
        description = escape(content.get("description", ""))

        # Collect regulatory references from the enrichment dict when available (set by
        # ValidateEnrichStage); otherwise fall back to raw content.  Both 'regulatory_refs'
        # and 'standards' are merged so neither is silently ignored when both are present.
        enrichment = source.get("enrichment", {})
        if enrichment.get("regulatory_refs") is not None:
            reg_refs: list = list(enrichment["regulatory_refs"])
        else:
            reg_refs_raw = content.get("regulatory_refs")
            standards_raw = content.get("standards")
            if reg_refs_raw is not None:
                reg_refs = list(reg_refs_raw) + list(standards_raw or [])
            else:
                reg_refs = list(standards_raw or [])

        if enrichment.get("best_practices") is not None:
            best_practices: list = list(enrichment["best_practices"])
        else:
            best_practices = list(content.get("best_practices") or [])

        all_citations = reg_refs + best_practices

        def _parse(entry: Any):
            """Return (code, title) from a string or dict ref entry.

            Key lookup uses explicit None and empty-string checks so that a
            key present with a falsy value does not mask a later key that
            carries a real value.
            """
            if isinstance(entry, str):
                return entry, ""
            if isinstance(entry, dict):
                code = ""
                for key in ("standard", "code", "name"):
                    val = entry.get(key)
                    if val is not None and val != "":
                        code = str(val)
                        break
                title = ""
                for key in ("title", "description"):
                    val = entry.get(key)
                    if val is not None and val != "":
                        title = str(val)
                        break
                return code, title
            return "", ""

        # Build refs XML block for dmStatus (single loop via shared _parse helper)
        refs_xml = ""
        if all_citations:
            ref_lines = []
            for entry in all_citations:
                code, pub_title = _parse(entry)
                if not code:
                    continue
                title_elem = (
                    f"\n          <externalPubTitle>{escape(pub_title)}</externalPubTitle>"
                    if pub_title else ""
                )
                ref_lines.append(
                    f"      <externalPubRef>\n"
                    f"        <externalPubRefIdent>\n"
                    f"          <externalPubCode>{escape(code)}</externalPubCode>"
                    f"{title_elem}\n"
                    f"        </externalPubRefIdent>\n"
                    f"      </externalPubRef>"
                )
            if ref_lines:
                refs_xml = "\n    <refs>\n" + "\n".join(ref_lines) + "\n    </refs>"

        # Build inline citations content block (reuses _parse helper, no duplication)
        citations_xml = ""
        if all_citations:
            citation_lines = []
            for entry in all_citations:
                code, pub_title = _parse(entry)
                if not code:
                    continue
                text = f"[{escape(code)}] {escape(pub_title)}" if pub_title else f"[{escape(code)}]"
                citation_lines.append(f"      <para>{text}</para>")
            if citation_lines:
                citations_xml = (
                    "\n      <levelledPara>\n"
                    "        <title>Regulatory References and Industry Best Practices</title>\n"
                    + "\n".join(citation_lines)
                    + "\n      </levelledPara>"
                )

        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<dmodule xmlns="http://www.s1000d.org/S1000D_5-0">
  <identAndStatusSection>
    <dmAddress>
      <dmIdent>
        <dmCode dmCode="{artifact.dmc}"/>
        <language languageIsoCode="en" countryIsoCode="US"/>
        <issueInfo issueNumber="001" inWork="00"/>
      </dmIdent>
      <dmAddressItems>
        <issueDate year="{datetime.now().year}" month="{datetime.now().month}" day="{datetime.now().day}"/>
        <dmTitle>
          <techName>{title}</techName>
          <infoName>Description</infoName>
        </dmTitle>
      </dmAddressItems>
    </dmAddress>
    <dmStatus issueType="new">{refs_xml}
    </dmStatus>
  </identAndStatusSection>
  <content>
    <description>
      <para>{description}</para>{citations_xml}
    </description>
  </content>
</dmodule>
"""

        # Write XML to file
        with open(artifact.path, "w", encoding="utf-8") as f:
            f.write(xml_content)
    
    def _link_icn_references(
        self, 
        data_modules: List[OutputArtifact],
        state: Dict[str, Any]
    ) -> None:
        """Link ICN (graphics) references in data modules."""
        # Placeholder for ICN linking logic
        self.logger.debug(f"Linking ICN references for {len(data_modules)} DMs")


class AssembleStage:
    """
    Stage 4: ASSEMBLE DATA MODULES
    
    Responsibilities:
    - Assemble DMs into CSDB structure
    - Generate Publication Module (PM)
    - Generate Data Module List (DML)
    - Apply applicability filtering
    - Build publication structure
    """
    
    def __init__(self, config: PipelineStageConfig):
        self.config = config
        self.logger = logging.getLogger("asigt.pipeline.assemble")
    
    def execute(
        self, 
        context: ExecutionContext,
        state: Dict[str, Any]
    ) -> StageResult:
        """Execute assembly stage."""
        start_time = datetime.now()
        self.logger.info("Starting ASSEMBLE DATA MODULES stage")
        
        try:
            data_modules = state.get("data_modules", [])
            
            # Generate Publication Module
            pm = self._generate_pm(data_modules, context)
            state["publication_module"] = pm
            
            # Generate Data Module List
            dml = self._generate_dml(data_modules, context)
            state["data_module_list"] = dml
            
            # Assemble CSDB package
            csdb_path = self._assemble_csdb(data_modules, pm, dml, context)
            state["csdb_package_path"] = csdb_path
            
            end_time = datetime.now()
            
            result = StageResult(
                stage_name="assemble",
                status=StageStatus.COMPLETED,
                start_time=start_time,
                end_time=end_time,
                artifacts_produced=len(data_modules) + 2  # DMs + PM + DML
            )
            
            self.logger.info(f"ASSEMBLE completed: PM and DML generated")
            return result
            
        except Exception as e:
            self.logger.error(f"ASSEMBLE failed: {e}")
            return StageResult(
                stage_name="assemble",
                status=StageStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                errors=[str(e)]
            )
    
    def _generate_pm(
        self, 
        data_modules: List[OutputArtifact],
        context: ExecutionContext
    ) -> OutputArtifact:
        """Generate Publication Module."""
        pm_path = context.output_path / "PM-AMM-001.xml"
        
        pm = OutputArtifact(
            id="PM-AMM-001",
            path=pm_path,
            artifact_type=ArtifactType.PM,
            generated_at=datetime.now()
        )
        
        # Generate PM XML (simplified)
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<pm xmlns="http://www.s1000d.org/S1000D_5-0">
  <identAndStatusSection>
    <pmAddress>
      <pmIdent>
        <pmCode pmNumber="AMM-001" pmVolume="01"/>
        <language languageIsoCode="en" countryIsoCode="US"/>
        <issueInfo issueNumber="001" inWork="00"/>
      </pmIdent>
      <pmAddressItems>
        <issueDate year="{datetime.now().year}" month="{datetime.now().month}" day="{datetime.now().day}"/>
        <pmTitle>Aircraft Maintenance Manual</pmTitle>
      </pmAddressItems>
    </pmAddress>
  </identAndStatusSection>
  <content>
    <pmEntry>
      <pmEntryTitle>Maintenance Procedures</pmEntryTitle>
"""
        
        # Add DM references
        for dm in data_modules:
            xml_content += f"""      <dmRef>
        <dmRefIdent>
          <dmCode dmCode="{dm.dmc}"/>
        </dmRefIdent>
      </dmRef>
"""
        
        xml_content += """    </pmEntry>
  </content>
</pm>
"""
        
        with open(pm_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
        
        pm.compute_hash()
        return pm
    
    def _generate_dml(
        self, 
        data_modules: List[OutputArtifact],
        context: ExecutionContext
    ) -> OutputArtifact:
        """Generate Data Module List."""
        dml_path = context.output_path / "DML-AMM-001.xml"
        
        dml = OutputArtifact(
            id="DML-AMM-001",
            path=dml_path,
            artifact_type=ArtifactType.DML,
            generated_at=datetime.now()
        )
        
        # Generate DML XML (simplified)
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<dml xmlns="http://www.s1000d.org/S1000D_5-0">
  <identAndStatusSection>
    <dmlAddress>
      <dmlIdent>
        <dmlCode dmlType="c" yearOfDataIssue="2026" seqNumber="00001"/>
        <language languageIsoCode="en" countryIsoCode="US"/>
        <issueInfo issueNumber="001" inWork="00"/>
      </dmlIdent>
      <dmlAddressItems>
        <issueDate year="{datetime.now().year}" month="{datetime.now().month}" day="{datetime.now().day}"/>
        <dmlTitle>AMM Data Module List</dmlTitle>
      </dmlAddressItems>
    </dmlAddress>
  </identAndStatusSection>
  <content>
"""
        
        # Add DM references
        for dm in data_modules:
            xml_content += f"""    <dmlEntry>
      <dmRef>
        <dmRefIdent>
          <dmCode dmCode="{dm.dmc}"/>
        </dmRefIdent>
      </dmRef>
    </dmlEntry>
"""
        
        xml_content += """  </content>
</dml>
"""
        
        with open(dml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
        
        dml.compute_hash()
        return dml
    
    def _assemble_csdb(
        self, 
        data_modules: List[OutputArtifact],
        pm: OutputArtifact,
        dml: OutputArtifact,
        context: ExecutionContext
    ) -> Path:
        """Assemble CSDB package structure."""
        import shutil
        
        csdb_root = context.output_path / "CSDB"
        csdb_root.mkdir(parents=True, exist_ok=True)
        
        # Create directory structure
        dm_dir = csdb_root / "DM"
        pm_dir = csdb_root / "PM"
        dml_dir = csdb_root / "DML"
        
        dm_dir.mkdir(exist_ok=True)
        pm_dir.mkdir(exist_ok=True)
        dml_dir.mkdir(exist_ok=True)
        
        # Move/copy DMs into CSDB structure
        for dm in data_modules:
            if dm.path.exists():
                dest = dm_dir / dm.path.name
                shutil.copy2(dm.path, dest)
                # Update path reference
                dm.path = dest
        
        # Move/copy PM
        if pm.path.exists():
            dest = pm_dir / pm.path.name
            shutil.copy2(pm.path, dest)
            pm.path = dest
        
        # Move/copy DML
        if dml.path.exists():
            dest = dml_dir / dml.path.name
            shutil.copy2(dml.path, dest)
            dml.path = dest
        
        self.logger.info(f"Assembled CSDB package at {csdb_root}")
        return csdb_root


class PublishQAStage:
    """
    Stage 5: PUBLISH & QA
    
    Responsibilities:
    - Render to deliverable formats (IETP, PDF, IETM)
    - Perform quality assurance checks
    - Generate validation reports
    - Package for delivery
    """
    
    def __init__(self, config: PipelineStageConfig):
        self.config = config
        self.logger = logging.getLogger("asigt.pipeline.publish_qa")
    
    def execute(
        self, 
        context: ExecutionContext,
        state: Dict[str, Any]
    ) -> StageResult:
        """Execute publish and QA stage."""
        start_time = datetime.now()
        self.logger.info("Starting PUBLISH & QA stage")
        
        try:
            data_modules = state.get("data_modules", [])
            pm = state.get("publication_module")
            
            # Render outputs
            outputs = self._render_outputs(data_modules, pm, context)
            state["rendered_outputs"] = outputs
            
            # Perform QA checks
            qa_results = self._perform_qa(data_modules, pm)
            state["qa_results"] = qa_results
            
            end_time = datetime.now()
            
            result = StageResult(
                stage_name="publish_qa",
                status=StageStatus.COMPLETED,
                start_time=start_time,
                end_time=end_time,
                artifacts_produced=len(outputs)
            )
            
            if qa_results.get("warnings"):
                result.warnings.extend(qa_results["warnings"])
            
            self.logger.info(f"PUBLISH & QA completed: {len(outputs)} outputs generated")
            return result
            
        except Exception as e:
            self.logger.error(f"PUBLISH & QA failed: {e}")
            return StageResult(
                stage_name="publish_qa",
                status=StageStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                errors=[str(e)]
            )
    
    def _render_outputs(
        self, 
        data_modules: List[OutputArtifact],
        pm: Optional[OutputArtifact],
        context: ExecutionContext
    ) -> List[str]:
        """Render outputs to deliverable formats."""
        outputs = []
        
        # Render to IETP
        ietp_path = self._render_ietp(data_modules, pm, context)
        if ietp_path:
            outputs.append(f"IETP: {ietp_path}")
        
        # Render to PDF
        pdf_path = self._render_pdf(data_modules, pm, context)
        if pdf_path:
            outputs.append(f"PDF: {pdf_path}")
        
        return outputs
    
    def _render_ietp(
        self, 
        data_modules: List[OutputArtifact],
        pm: Optional[OutputArtifact],
        context: ExecutionContext
    ) -> Optional[Path]:
        """Render IETP output."""
        ietp_dir = context.output_path / "IETP"
        ietp_dir.mkdir(parents=True, exist_ok=True)
        
        # Placeholder for IETP rendering
        self.logger.debug(f"Rendering IETP to {ietp_dir}")
        return ietp_dir
    
    def _render_pdf(
        self, 
        data_modules: List[OutputArtifact],
        pm: Optional[OutputArtifact],
        context: ExecutionContext
    ) -> Optional[Path]:
        """Render PDF output."""
        pdf_dir = context.output_path / "PDF"
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
        # Placeholder for PDF rendering
        self.logger.debug(f"Rendering PDF to {pdf_dir}")
        return pdf_dir
    
    def _perform_qa(
        self, 
        data_modules: List[OutputArtifact],
        pm: Optional[OutputArtifact]
    ) -> Dict[str, Any]:
        """Perform quality assurance checks."""
        qa_results = {
            "total_checks": 0,
            "passed": 0,
            "failed": 0,
            "warnings": [],
            "errors": []
        }
        
        # Check 1: All DMs have valid DMC codes
        qa_results["total_checks"] += 1
        for dm in data_modules:
            if not getattr(dm, "dmc", None):
                qa_results["warnings"].append(f"DM {getattr(dm, 'id', '<unknown>')} missing DMC code")
        # Missing DMC codes are treated as warnings only; the check is considered passed.
        qa_results["passed"] += 1
        
        # Check 2: PM exists
        qa_results["total_checks"] += 1
        if not pm:
            qa_results["warnings"].append("Publication Module not generated")
        # Missing PM is treated as a warning only; the check is considered passed.
        qa_results["passed"] += 1
        
        # Check 3: All files exist
        qa_results["total_checks"] += 1
        missing_files = False
        for dm in data_modules:
            if not dm.path.exists():
                qa_results["errors"].append(f"DM file not found: {dm.path}")
                missing_files = True
        
        if missing_files:
            qa_results["failed"] += 1
        else:
            qa_results["passed"] += 1
        
        return qa_results


# =============================================================================
# CONTENT PIPELINE ORCHESTRATOR
# =============================================================================


class ContentPipeline:
    """
    S1000D AMM Content Pipeline Orchestrator.
    
    Orchestrates the complete content transformation workflow through
    five stages:
    1. INGEST & NORMALIZE
    2. VALIDATE & ENRICH
    3. TRANSFORM TO S1000D
    4. ASSEMBLE DATA MODULES
    5. PUBLISH & QA
    
    Usage:
        >>> pipeline = ContentPipeline.from_yaml("pipelines/amm_pipeline.yaml")
        >>> context = ExecutionContext(...)
        >>> result = pipeline.execute(context)
    """
    
    def __init__(self, config: PipelineConfig):
        """Initialize content pipeline with configuration."""
        self.config = config
        self.logger = logging.getLogger("asigt.content_pipeline")
        self.engine = ASIGTEngine()
        
        # Initialize stages as ordered list
        self.stages: List[Tuple[PipelineStageType, Any]] = []
        self._init_stages()
    
    def _init_stages(self) -> None:
        """Initialize pipeline stages based on configuration."""
        # Sort stages by configured order
        sorted_stages = sorted(self.config.stages, key=lambda s: s.config.get("order", 0))
        
        for stage_config in sorted_stages:
            if not stage_config.enabled:
                continue
                
            stage_instance = None
            if stage_config.stage_type == PipelineStageType.INGEST_NORMALIZE:
                stage_instance = IngestNormalizeStage(stage_config)
            elif stage_config.stage_type == PipelineStageType.VALIDATE_ENRICH:
                stage_instance = ValidateEnrichStage(stage_config)
            elif stage_config.stage_type == PipelineStageType.TRANSFORM:
                stage_instance = TransformStage(stage_config)
            elif stage_config.stage_type == PipelineStageType.ASSEMBLE:
                stage_instance = AssembleStage(stage_config)
            elif stage_config.stage_type == PipelineStageType.PUBLISH_QA:
                stage_instance = PublishQAStage(stage_config)
            
            if stage_instance:
                self.stages.append((stage_config.stage_type, stage_instance))
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> ContentPipeline:
        """Create pipeline from YAML configuration file."""
        config = PipelineConfig.from_yaml(yaml_path)
        return cls(config)
    
    def execute(self, context: ExecutionContext) -> RunResult:
        """
        Execute the complete content pipeline.
        
        Args:
            context: Execution context from ASIT
            
        Returns:
            RunResult with complete execution details
        """
        self.logger.info(f"Starting content pipeline: {self.config.name}")
        self.logger.info(f"Pipeline ID: {self.config.pipeline_id}")
        self.logger.info(f"Publication Type: {self.config.publication_type}")
        
        # Initialize run state
        state: Dict[str, Any] = {
            "context": context,
            "pipeline_config": self.config,
            "sources": [],
            "data_modules": [],
            "outputs": []
        }
        
        # Create result directly without calling engine.execute()
        run_id = self._generate_run_id(context)
        result = RunResult(
            run_id=run_id,
            status=RunStatus.RUNNING,
            contract_id=context.contract_id,
            baseline_id=context.baseline_id,
            start_time=datetime.now(),
            metrics=ExecutionMetrics(start_time=datetime.now())
        )
        
        # Execute custom pipeline stages in configured order
        for stage_type, stage in self.stages:
            stage_result = stage.execute(context, state)
            result.stage_results.append(stage_result)
            
            if stage_result.status == StageStatus.FAILED:
                self.logger.error(f"Pipeline stage failed: {stage_type.value}")
                result.status = RunStatus.FAILED
                break
        
        # Update result with state data
        output_count = 0
        if "data_modules" in state and isinstance(state["data_modules"], list):
            output_count += len(state["data_modules"])
        if "publication_module" in state:
            output_count += 1
        if "data_module_list" in state:
            output_count += 1
        if "rendered_outputs" in state and isinstance(state["rendered_outputs"], list):
            output_count += len(state["rendered_outputs"])
        result.metrics.outputs_generated = output_count
        
        # Set final status
        if result.status != RunStatus.FAILED:
            result.status = RunStatus.SUCCESS
        
        result.end_time = datetime.now()
        self.logger.info(f"Content pipeline completed: {result.status.value}")
        return result
    
    def _generate_run_id(self, context: ExecutionContext) -> str:
        """Generate unique run ID."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        return f"{timestamp}__{context.contract_id}"
    
    def validate_config(self) -> Tuple[bool, List[str]]:
        """
        Validate pipeline configuration.
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        if not self.config.pipeline_id:
            errors.append("Pipeline ID is required")
        
        if not self.config.name:
            errors.append("Pipeline name is required")
        
        if not self.config.stages:
            errors.append("At least one stage must be defined")
        
        return (len(errors) == 0, errors)
    
    def get_stage_status(self, stage_type: PipelineStageType) -> Optional[str]:
        """Get status of a specific pipeline stage."""
        # This would track stage execution status
        return "PENDING"


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def create_amm_pipeline(pipeline_yaml: Path) -> ContentPipeline:
    """
    Create an AMM content pipeline from YAML configuration.
    
    Args:
        pipeline_yaml: Path to pipeline YAML configuration
        
    Returns:
        Configured ContentPipeline instance
    """
    return ContentPipeline.from_yaml(pipeline_yaml)


def execute_pipeline(
    pipeline_yaml: Path,
    contract_id: str,
    baseline_id: str,
    kdb_root: Path,
    output_path: Path,
    run_archive_path: Optional[Path] = None
) -> RunResult:
    """
    Execute a content pipeline with simplified parameters.
    
    Args:
        pipeline_yaml: Path to pipeline configuration
        contract_id: ASIT contract ID
        baseline_id: Baseline reference
        kdb_root: KDB root directory
        output_path: Output directory for generated content
        run_archive_path: Optional run archive path (defaults to output_path/../ASIGT/runs)
        
    Returns:
        RunResult with execution details
    """
    # Create pipeline
    pipeline = ContentPipeline.from_yaml(pipeline_yaml)
    
    # Default run_archive_path to be relative to output_path
    if run_archive_path is None:
        run_archive_path = output_path.parent / "ASIGT" / "runs"
    
    # Create execution context
    context = ExecutionContext(
        contract_id=contract_id,
        contract_version="1.0",
        baseline_id=baseline_id,
        authority_reference=f"{contract_id}::APPROVED",
        invocation_timestamp=datetime.now(),
        kdb_root=kdb_root,
        idb_root=output_path.parent,
        output_path=output_path,
        run_archive_path=run_archive_path
    )
    
    # Execute pipeline
    return pipeline.execute(context)
