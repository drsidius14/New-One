#!/usr/bin/env python3
"""Apply translations as Android values-ru overlays and copy targeted text asset overrides."""
from __future__ import annotations
import argparse, json, os, re, shutil
from pathlib import Path
import xml.etree.ElementTree as ET

KINDS={'strings':'string','string_arrays':'string-array','plurals':'plurals'}
PLACEHOLDER=re.compile(r'%(?:[0-9]+\$)?[-#+ 0,(]*[0-9]*(?:\.[0-9]+)?[tT]?[a-zA-Z]')

def local_name(el):
    tag=el.tag
    if tag=='item' and el.get('type')=='string': tag='string'
    return tag,el.get('name')

def text_of(el): return ''.join(el.itertext())

def scan_resources(res_dir):
    found={k:{} for k in KINDS.values()}
    for path in res_dir.glob('values*/*.xml'):
        try: root=ET.parse(path).getroot()
        except ET.ParseError as e: raise RuntimeError(f'Invalid resource XML {path}: {e}')
        for el in root:
            kind,name=local_name(el)
            if not name or kind not in found: continue
            if kind not in ('string','string-array','plurals'): continue
            if kind=='string':
                val=text_of(el)
            elif kind=='string-array':
                val=[text_of(i) for i in el.findall('item')]
            elif kind=='plurals':
                val={i.get('quantity',''):text_of(i) for i in el.findall('item')}
            else:
                continue
            found[kind].setdefault(name,[]).append(val)
    return found

def placeholders(s): return sorted(PLACEHOLDER.findall(s or ''))

def validate_translation(key,value,kind,source_values):
    if isinstance(value,str):
        if not value.strip(): raise RuntimeError(f'Empty Russian translation: {kind}:{key}')
        if isinstance(source_values,list) and source_values:
            for source in source_values:
                st=source if isinstance(source,str) else ''
                if placeholders(st)!=placeholders(value):
                    raise RuntimeError(f'Placeholder mismatch for {kind}:{key}: source {placeholders(st)} vs translation {placeholders(value)}')
    elif kind=='string_arrays':
        if not isinstance(value,list) or not value or any(not isinstance(x,str) or not x.strip() for x in value):
            raise RuntimeError(f'{kind}:{key} must be a non-empty array of non-empty strings')
        # Array source counts may differ by locale; require a matching source count if present.
        source_arrays=[v for v in source_values if isinstance(v,list)]
        counts=[len(v) for v in source_arrays]
        if counts and len(value) not in set(counts):
            raise RuntimeError(f'{kind}:{key} has {len(value)} items; source arrays have counts {sorted(set(counts))}')
        for index,translated in enumerate(value):
            expected={tuple(placeholders(src[index])) for src in source_arrays if index < len(src)}
            if expected and tuple(placeholders(translated)) not in expected:
                raise RuntimeError(f'Placeholder mismatch for {kind}:{key}[{index}]')
    elif kind=='plurals':
        if not isinstance(value,dict) or not {'one','few','many','other'}.issubset(value):
            raise RuntimeError(f'{kind}:{key} must define Russian quantities one, few, many and other')
        if any(not isinstance(v,str) or not v.strip() for v in value.values()):
            raise RuntimeError(f'{kind}:{key} contains an empty/non-string quantity')
        source_plurals=[v for v in source_values if isinstance(v,dict)]
        expected={tuple(placeholders(text)) for src in source_plurals for text in src.values()}
        for quantity,translated in value.items():
            if expected and tuple(placeholders(translated)) not in expected:
                raise RuntimeError(f'Placeholder mismatch for {kind}:{key}[{quantity}]')
    else: raise RuntimeError(f'Unsupported patch kind: {kind}')

def merge_resource_file(path, kind, translations):
    if not translations: return
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists(): root=ET.parse(path).getroot()
    else: root=ET.Element('resources')
    tag_to_existing={ (el.tag if el.tag!='item' else ('string' if el.get('type')=='string' else 'item'),el.get('name')):el for el in list(root) if el.get('name') }
    for name,value in translations.items():
        tag='string' if kind=='strings' else ('string-array' if kind=='string_arrays' else 'plurals')
        old=tag_to_existing.get((tag,name))
        if old is not None: root.remove(old)
        if tag=='string':
            el=ET.SubElement(root,'string',{'name':name}); el.text=value
        elif tag=='string-array':
            el=ET.SubElement(root,'string-array',{'name':name})
            for text in value: ET.SubElement(el,'item').text=text
        else:
            el=ET.SubElement(root,'plurals',{'name':name})
            for quantity in ('zero','one','two','few','many','other'):
                if quantity in value: ET.SubElement(el,'item',{'quantity':quantity}).text=value[quantity]
    ET.indent(root,space='    ')
    ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root',required=True)
    ap.add_argument('--decoded-dir',required=True)
    a=ap.parse_args()
    project=Path(a.project_root).resolve(); decoded=Path(a.decoded_dir).resolve()
    patch_path=project/'patches/ru/resources.json'
    patch=json.loads(patch_path.read_text(encoding='utf-8'))
    for section in KINDS:
        if section not in patch or not isinstance(patch[section],dict): raise RuntimeError(f'{patch_path}: expected object field "{section}"')
    source=scan_resources(decoded/'res')
    count=0
    for section,kind in KINDS.items():
        translations=patch[section]
        for name,value in translations.items():
            if name not in source[kind]: raise RuntimeError(f'Patch target does not exist in this exact APK: {kind}:{name}')
            validate_translation(name,value,section,source[kind][name])
        if translations:
            target=decoded/'res'/'values-ru'/({'strings':'strings.xml','string_arrays':'arrays.xml','plurals':'plurals.xml'}[section])
            merge_resource_file(target,section,translations)
            count+=len(translations)
    # Asset overrides mirror paths under decoded/assets. Only existing source assets may be overridden.
    overrides=project/'patches/ru/assets/overrides'
    asset_count=0
    if overrides.exists():
        base_assets=(decoded/'assets').resolve()
        for src in sorted(overrides.rglob('*')):
            if not src.is_file(): continue
            rel=src.relative_to(overrides)
            dest=(base_assets/rel).resolve()
            if base_assets not in dest.parents: raise RuntimeError(f'Asset override path escapes assets/: {rel}')
            if not dest.is_file(): raise RuntimeError(f'Asset override target absent in this base APK: assets/{rel.as_posix()}')
            if src.suffix.lower() not in {'.html','.htm','.txt','.json','.xml','.js','.css','.csv','.md','.properties'}:
                raise RuntimeError(f'Non-text asset override is not allowed: {rel}')
            src.read_text(encoding='utf-8')
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(src,dest)
            asset_count+=1
    print(f'Russian Android resource translations applied: {count}')
    print(f'Text asset overrides applied: {asset_count}')
    out=os.environ.get('GITHUB_OUTPUT')
    if out:
        with open(out,'a',encoding='utf-8') as f:
            f.write(f'resource_count={count}\nasset_override_count={asset_count}\n')
if __name__=='__main__': main()
