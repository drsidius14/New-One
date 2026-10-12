#!/usr/bin/env python3
"""Record every decoded APK file before applying localization changes."""
import argparse, hashlib, json
from pathlib import Path

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(); p.add_argument('--decoded-dir',required=True); p.add_argument('--output',required=True); a=p.parse_args()
    root=Path(a.decoded_dir).resolve()
    if not root.is_dir(): raise RuntimeError(f'Decoded directory missing: {root}')
    data={x.relative_to(root).as_posix():digest(x) for x in sorted(root.rglob('*')) if x.is_file()}
    Path(a.output).write_text(json.dumps(data,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(f'Snapshotted {len(data)} decoded files.')
if __name__=='__main__': main()
