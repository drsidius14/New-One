#!/usr/bin/env python3
"""Fail closed unless the repository contains the exact supplied base APK."""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    args=ap.parse_args()
    root=Path(args.project_root).resolve()
    config=json.loads((root/'config/project.json').read_text(encoding='utf-8'))
    apk=(root/config['base_apk']).resolve()
    if not apk.is_file():
        raise RuntimeError(f'Base APK is missing: {apk}')
    actual=sha256(apk)
    expected=config['base_sha256']
    if actual.lower()!=expected.lower():
        raise RuntimeError(f'BASE APK SHA-256 MISMATCH: expected {expected}, got {actual}; refusing to continue')
    with zipfile.ZipFile(apk) as z:
        names=set(z.namelist())
        manifest=z.read('AndroidManifest.xml') if 'AndroidManifest.xml' in names else b''
        package_bytes=config['package_name']
        if not any(package_bytes.encode(encoding) in manifest for encoding in ('utf-8','utf-16le','utf-16be')):
            raise RuntimeError('Configured package name was not found in this APK manifest; refusing to continue')
        required={'AndroidManifest.xml','resources.arsc','classes.dex'}
        missing=required-names
        if missing:
            raise RuntimeError('APK is missing required entries: '+', '.join(sorted(missing)))
        dex=sorted(n for n in names if n.startswith('classes') and n.endswith('.dex'))
        abis=sorted({n.split('/')[1] for n in names if n.startswith('lib/') and n.endswith('.so') and len(n.split('/'))>=3})
        signer_files=sorted(n for n in names if n.startswith('META-INF/') and n.upper().endswith(('.RSA','.DSA','.EC')))
        print('Base APK verified')
        print('File:', config['base_apk'])
        print('SHA-256:', actual)
        print('Package configured:', config['package_name'])
        print('Version:', config['version_name'], '(code', config['version_code'], ')')
        print('DEX files:', ', '.join(dex))
        print('Native ABIs:', ', '.join(abis))
        print('V1 signer files:', ', '.join(signer_files) if signer_files else 'not present')
    return 0
if __name__=='__main__':
    main()
