#!/usr/bin/env python3
"""Fast syntax and resource-target validation for patch sources."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import xml.etree.ElementTree as ET

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',required=True); ap.add_argument('--decoded-dir')
    a=ap.parse_args(); root=Path(a.project_root).resolve()
    config=json.loads((root/'config/project.json').read_text(encoding='utf-8'))
    if config['package_name']!='com.mi.healthresearch' or config['version_name']!='1.4.6':
        raise RuntimeError('Project identity changed; refusing to validate as the requested base APK')
    patches=json.loads((root/'patches/ru/resources.json').read_text(encoding='utf-8'))
    expected={'strings','string_arrays','plurals'}
    if set(patches)!=expected: raise RuntimeError(f'Patch schema must contain exactly {sorted(expected)}')
    if a.decoded_dir:
        res=Path(a.decoded_dir).resolve()/'res'
        available=set()
        for path in res.glob('values*/*.xml'):
            tree=ET.parse(path)
            for e in tree.getroot():
                tag=e.tag
                if tag=='item' and e.get('type')=='string': tag='string'
                available.add((tag,e.get('name')))
        for key in patches['strings']:
            if ('string',key) not in available: raise RuntimeError(f'Unknown resource string: {key}')
        for key in patches['string_arrays']:
            if ('string-array',key) not in available: raise RuntimeError(f'Unknown string-array: {key}')
        for key in patches['plurals']:
            if ('plurals',key) not in available: raise RuntimeError(f'Unknown plurals resource: {key}')
    override_root=root/'patches/ru/assets/overrides'
    for path in override_root.rglob('*') if override_root.exists() else []:
        if path.is_file():
            if path.suffix.lower() not in {'.html','.htm','.txt','.json','.xml','.js','.css','.csv','.md','.properties'}: raise RuntimeError(f'Unsupported asset override extension: {path}')
            path.read_text(encoding='utf-8')
    print('Patch JSON, project identity and text asset overrides are valid.')
if __name__=='__main__': main()
