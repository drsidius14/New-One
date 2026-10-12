#!/usr/bin/env python3
"""Fail closed if localization patch changes anything outside the approved resource files."""
import argparse, hashlib, json
from pathlib import Path

ALLOWED={
 'res/values-ru/strings.xml',
 'res/values-ru/arrays.xml',
 'res/values-ru/plurals.xml',
}
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(); p.add_argument('--decoded-dir',required=True); p.add_argument('--snapshot',required=True); a=p.parse_args()
    root=Path(a.decoded_dir).resolve(); before=json.loads(Path(a.snapshot).read_text(encoding='utf-8'))
    after={x.relative_to(root).as_posix():digest(x) for x in sorted(root.rglob('*')) if x.is_file()}
    changed=[]
    for rel in sorted(set(before)|set(after)):
        if before.get(rel)!=after.get(rel): changed.append(rel)
    forbidden=[x for x in changed if x not in ALLOWED]
    if forbidden:
        raise RuntimeError('Unexpected decoded APK modifications (build blocked):\n'+'\n'.join(forbidden))
    print('Decoded patch scope audit passed.')
    print('Changed approved localization files: '+(', '.join(changed) if changed else 'none'))
    print('DEX/smali, manifest, native libraries, assets and all other decoded files are unchanged.')
if __name__=='__main__': main()
