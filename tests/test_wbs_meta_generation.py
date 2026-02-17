"""
Test suite for WBS meta file generation script.

Tests the generate_wbs_meta_files.py script functionality.
"""

import os
import sys
import tempfile
import pytest
import yaml
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from generate_wbs_meta_files import (
    get_file_type_from_extension,
    extract_lc_phase_from_path,
    extract_file_id_from_path,
    generate_meta_content,
    process_work_package
)


class TestFileUtilities:
    """Test utility functions for file processing."""
    
    def test_get_file_type_from_extension(self):
        """Test file type detection from extensions."""
        assert get_file_type_from_extension('model.step') == 'CAD_MODEL'
        assert get_file_type_from_extension('data.yaml') == 'DATA_FILE'
        assert get_file_type_from_extension('data.csv') == 'DATA_FILE'
        assert get_file_type_from_extension('report.pdf') == 'DOCUMENT'
        assert get_file_type_from_extension('readme.md') == 'DOCUMENT'
        assert get_file_type_from_extension('model.nas') == 'FEM_MODEL'
        assert get_file_type_from_extension('model.inp') == 'FEM_MODEL'
        assert get_file_type_from_extension('drawing.dxf') == 'CAD_DRAWING'
        assert get_file_type_from_extension('diagram.svg') == 'DIAGRAM'
        assert get_file_type_from_extension('calc.xlsx') == 'SPREADSHEET'
        assert get_file_type_from_extension('unknown.xyz') == 'FILE'
    
    def test_extract_lc_phase_from_path(self):
        """Test lifecycle phase extraction from file paths."""
        assert extract_lc_phase_from_path('LC04_DESIGN_DEFINITION/file.yaml') == 'LC04_DESIGN_DEFINITION'
        assert extract_lc_phase_from_path('LC05_VERIFICATION_VALIDATION/file.yaml') == 'LC05_VERIFICATION_VALIDATION'
        assert extract_lc_phase_from_path('other/file.yaml') == 'LC04'  # default
    
    def test_extract_file_id_from_path(self):
        """Test file ID extraction from paths."""
        assert extract_file_id_from_path('path/to/GEOM-28-11-00-C2-CELL.step') == 'GEOM-28-11-00-C2-CELL'
        assert extract_file_id_from_path('path/to/GEOM-28-11-00-C2-CELL.params.yaml') == 'GEOM-28-11-00-C2-CELL'
        assert extract_file_id_from_path('path/to/report.pdf') == 'report'


class TestMetaGeneration:
    """Test meta file content generation."""
    
    def test_generate_meta_content(self):
        """Test generation of meta file content."""
        work_package = {
            'id': 'WP-28-03-01',
            'title': 'Cell Design',
            'owner': 'STK_ENG',
            'revision': '0.1.0',
            'status': 'draft',
            'ata': '28-11-00',
            'domain': 'C2-CIRCULAR_CRYOGENIC_CELLS',
            'tags': ['cryogenic', 'LH2']
        }
        
        output = {
            'id': 'geometry_definition',
            'formats': ['CAD_STEP_AP242', 'parameter_table_YAML']
        }
        
        file_path = 'LC04_DESIGN_DEFINITION/ATA_28-11-00/WP-28-03-01/geometry/GEOM-28-11-00-C2-CELL.step'
        
        meta = generate_meta_content(file_path, work_package, output)
        
        assert meta['id'] == 'GEOM-28-11-00-C2-CELL'
        assert meta['type'] == 'CAD_MODEL'
        assert meta['title'] == 'Cell Design - geometry_definition'
        assert meta['owner'] == 'STK_ENG'
        assert meta['revision'] == '0.1.0'
        assert meta['status'] == 'draft'
        assert meta['lc_phase'] == 'LC04_DESIGN_DEFINITION'
        assert meta['work_package'] == 'WP-28-03-01'
        assert meta['ata'] == '28-11-00'
        assert meta['domain'] == 'C2-CIRCULAR_CRYOGENIC_CELLS'
        assert 'cryogenic' in meta['tags']
        assert 'LH2' in meta['tags']
        assert meta['integrity']['algorithm'] == 'sha256'
        assert 'to be generated' in meta['integrity']['checksum']


class TestWorkPackageProcessing:
    """Test work package processing."""
    
    def test_process_work_package_dry_run(self):
        """Test processing a work package in dry-run mode."""
        work_package = {
            'id': 'WP-TEST-01',
            'title': 'Test Package',
            'owner': 'STK_ENG',
            'revision': '0.1.0',
            'status': 'draft',
            'ata': '28-11-00',
            'domain': 'TEST',
            'tags': ['test'],
            'outputs': [
                {
                    'id': 'test_output',
                    'formats': ['test_format'],
                    'files': ['test_file.yaml'],
                    'meta_file': 'test_file.meta.yaml'
                }
            ],
            'verification': []
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            generated = process_work_package(work_package, base_path, dry_run=True)
            
            assert len(generated) == 1
            assert 'test_file.meta.yaml' in generated[0]
    
    def test_process_work_package_creates_files(self):
        """Test that processing actually creates files."""
        work_package = {
            'id': 'WP-TEST-02',
            'title': 'Test Package 2',
            'owner': 'STK_SAF',
            'revision': '0.2.0',
            'status': 'draft',
            'ata': '28-41-00',
            'domain': 'TEST',
            'tags': ['test'],
            'outputs': [
                {
                    'id': 'sensor_output',
                    'formats': ['YAML'],
                    'files': ['LC04/sensor.yaml', 'LC04/sensor.pdf'],
                    'meta_file': 'LC04/sensor.meta.yaml'
                }
            ],
            'verification': [
                {'id': 'test_verification'}
            ]
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            generated = process_work_package(work_package, base_path, dry_run=False)
            
            assert len(generated) == 1
            meta_file = Path(generated[0])
            assert meta_file.exists()
            
            # Verify content
            with open(meta_file, 'r') as f:
                meta_content = yaml.safe_load(f)
            
            assert meta_content['output_id'] == 'sensor_output'
            assert meta_content['work_package'] == 'WP-TEST-02'
            assert meta_content['owner'] == 'STK_SAF'
            assert meta_content['ata'] == '28-41-00'
            assert len(meta_content['files']) == 2
            assert 'test_verification' in meta_content['links']['verification']


class TestIntegrity:
    """Test integrity and consistency checks."""
    
    def test_meta_files_have_required_fields(self):
        """Test that all generated meta files have required fields."""
        required_fields = [
            'output_id', 'work_package', 'title', 'owner', 'revision',
            'status', 'lc_phase', 'ata', 'domain', 'created_on',
            'last_updated_on', 'integrity', 'links', 'tags', 'formats', 'files'
        ]
        
        work_package = {
            'id': 'WP-TEST-03',
            'title': 'Integrity Test',
            'owner': 'STK_ENG',
            'revision': '1.0.0',
            'status': 'released',
            'ata': '28-00-00',
            'domain': 'TEST',
            'tags': ['integrity'],
            'outputs': [
                {
                    'id': 'integrity_check',
                    'formats': ['YAML'],
                    'files': ['test.yaml'],
                    'meta_file': 'test.meta.yaml'
                }
            ],
            'verification': []
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            generated = process_work_package(work_package, base_path, dry_run=False)
            
            meta_file = Path(generated[0])
            with open(meta_file, 'r') as f:
                meta_content = yaml.safe_load(f)
            
            for field in required_fields:
                assert field in meta_content, f"Missing required field: {field}"
            
            # Check nested integrity fields
            assert 'checksum' in meta_content['integrity']
            assert 'algorithm' in meta_content['integrity']
            
            # Check nested links fields
            assert 'reqs' in meta_content['links']
            assert 'safety' in meta_content['links']
            assert 'work_package' in meta_content['links']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
