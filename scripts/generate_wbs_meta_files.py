#!/usr/bin/env python3
"""
Generate .meta.yaml sidecar files for WBS Level 2 outputs.

This script parses the WBS_LEVEL_2.yaml file and generates corresponding
.meta.yaml files for all output files specified in the work packages.
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


def get_file_type_from_extension(file_path: str) -> str:
    """Determine file type from file extension."""
    ext = Path(file_path).suffix.lower()
    
    type_map = {
        '.step': 'CAD_MODEL',
        '.yaml': 'DATA_FILE',
        '.csv': 'DATA_FILE',
        '.pdf': 'DOCUMENT',
        '.md': 'DOCUMENT',
        '.nas': 'FEM_MODEL',
        '.inp': 'FEM_MODEL',
        '.dxf': 'CAD_DRAWING',
        '.svg': 'DIAGRAM',
        '.xlsx': 'SPREADSHEET',
    }
    
    return type_map.get(ext, 'FILE')


def extract_lc_phase_from_path(file_path: str) -> str:
    """Extract lifecycle phase from file path."""
    path_parts = file_path.split('/')
    if path_parts:
        first_part = path_parts[0]
        if first_part.startswith('LC'):
            return first_part
    return 'LC04'  # default


def extract_file_id_from_path(file_path: str) -> str:
    """Extract a meaningful ID from the file path."""
    filename = Path(file_path).stem
    # Remove extensions like .params, .meta
    if '.' in filename:
        parts = filename.split('.')
        filename = parts[0]
    return filename


def generate_meta_content(
    file_path: str,
    work_package: Dict[str, Any],
    output: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate the content for a .meta.yaml file."""
    
    file_id = extract_file_id_from_path(file_path)
    file_type = get_file_type_from_extension(file_path)
    lc_phase = extract_lc_phase_from_path(file_path)
    
    meta_content = {
        'id': file_id,
        'type': file_type,
        'title': f"{work_package['title']} - {output['id']}",
        'owner': work_package['owner'],
        'revision': work_package.get('revision', '0.1.0'),
        'status': work_package.get('status', 'draft'),
        'lc_phase': lc_phase,
        'work_package': work_package['id'],
        'ata': work_package.get('ata', '28-00-00'),
        'domain': work_package.get('domain', 'C2-CIRCULAR_CRYOGENIC_CELLS'),
        'created_on': 'to be set during baseline finalization',
        'last_updated_on': 'to be set during baseline finalization',
        'integrity': {
            'checksum': 'to be generated upon baseline finalization',
            'algorithm': 'sha256'
        },
        'links': {
            'reqs': [],
            'safety': [],
            'work_package': work_package['id'],
            'output_id': output['id']
        },
        'tags': work_package.get('tags', []),
        'file_path': file_path,
        'formats': output.get('formats', [])
    }
    
    return meta_content


def process_work_package(
    work_package: Dict[str, Any],
    base_path: Path,
    dry_run: bool = False
) -> List[str]:
    """Process a single work package and generate meta files for its outputs."""
    
    generated_files = []
    
    if 'outputs' not in work_package:
        return generated_files
    
    for output in work_package['outputs']:
        if 'meta_file' not in output:
            continue
            
        meta_file_path = base_path / output['meta_file']
        
        # Generate meta content (aggregate for all files in this output)
        files_metadata = []
        for file_path in output.get('files', []):
            file_meta = {
                'file': file_path,
                'id': extract_file_id_from_path(file_path),
                'type': get_file_type_from_extension(file_path)
            }
            files_metadata.append(file_meta)
        
        # Create the main meta content
        meta_content = {
            'output_id': output['id'],
            'work_package': work_package['id'],
            'title': f"{work_package['title']} - {output['id']}",
            'owner': work_package['owner'],
            'revision': work_package.get('revision', '0.1.0'),
            'status': work_package.get('status', 'draft'),
            'lc_phase': extract_lc_phase_from_path(output['meta_file']),
            'ata': work_package.get('ata', '28-00-00'),
            'domain': work_package.get('domain', 'C2-CIRCULAR_CRYOGENIC_CELLS'),
            'created_on': 'to be set during baseline finalization',
            'last_updated_on': 'to be set during baseline finalization',
            'integrity': {
                'checksum': 'to be generated upon baseline finalization',
                'algorithm': 'sha256'
            },
            'links': {
                'reqs': [],
                'safety': [],
                'work_package': work_package['id'],
                'verification': [v['id'] for v in work_package.get('verification', [])]
            },
            'tags': work_package.get('tags', []),
            'formats': output.get('formats', []),
            'files': files_metadata
        }
        
        if not dry_run:
            # Create directory if it doesn't exist
            meta_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the meta file
            with open(meta_file_path, 'w', encoding='utf-8') as f:
                yaml.dump(meta_content, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
            generated_files.append(str(meta_file_path))
            print(f"✓ Generated: {meta_file_path}")
        else:
            print(f"  Would generate: {meta_file_path}")
            generated_files.append(str(meta_file_path))
    
    return generated_files


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate .meta.yaml files for WBS outputs')
    parser.add_argument('--wbs-file', default='OPT-IN_FRAMEWORK/T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS/C2-CIRCULAR_CRYOGENIC_CELLS/ATA_28-FUEL/WBS/WBS_LEVEL_2.yaml',
                        help='Path to WBS_LEVEL_2.yaml file')
    parser.add_argument('--base-path', default='OPT-IN_FRAMEWORK/T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS/C2-CIRCULAR_CRYOGENIC_CELLS/ATA_28-FUEL',
                        help='Base path for output files')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be generated without creating files')
    
    args = parser.parse_args()
    
    # Get repository root
    repo_root = Path(__file__).parent.parent
    wbs_file = repo_root / args.wbs_file
    base_path = repo_root / args.base_path
    
    if not wbs_file.exists():
        print(f"Error: WBS file not found: {wbs_file}", file=sys.stderr)
        sys.exit(1)
    
    # Load WBS file
    print(f"Loading WBS file: {wbs_file}")
    with open(wbs_file, 'r', encoding='utf-8') as f:
        wbs_data = yaml.safe_load(f)
    
    if not wbs_data or 'work_packages' not in wbs_data:
        print("Error: Invalid WBS file format", file=sys.stderr)
        sys.exit(1)
    
    # Process all work packages
    all_generated_files = []
    for work_package in wbs_data['work_packages']:
        wp_id = work_package.get('id', 'UNKNOWN')
        print(f"\nProcessing {wp_id}: {work_package.get('title', 'No title')}")
        
        generated = process_work_package(work_package, base_path, args.dry_run)
        all_generated_files.extend(generated)
    
    # Summary
    print(f"\n{'Would generate' if args.dry_run else 'Generated'} {len(all_generated_files)} .meta.yaml files")
    
    if args.dry_run:
        print("\nRun without --dry-run to actually create the files.")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
