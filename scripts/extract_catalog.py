#!/usr/bin/env python3
"""Export Android string resources and readable assets for human translation review."""
from __future__ import annotations
import argparse, csv, json, re, shutil
from pathlib import Path
import xml.etree.ElementTree as ET

TEXT_EXTS={'.html','.htm','.txt','.json','.xml','.js','.css','.csv','.md','.properties'}
CJK=re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff]')
RESOURCE_TAGS={'string','string-array','plurals'}

def element_value(el, kind):
    if kind=='string':
        return ''.join(el.itertext())
    if kind=='string-array':
        return [ ''.join(item.itertext()) for item in el.findall('item') ]
    if kind=='plurals':
        return {item.get('quantity',''):''.join(item.itertext()) for item in el.findall('item')}
    return ''.join(el.itertext())

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--decoded-dir',required=True)
    p.add_argument('--out-dir',required=True)
    a=p.parse_args()
    decoded=Path(a.decoded_dir).resolve(); out=Path(a.out_dir).resolve()
    res=decoded/'res'; assets=decoded/'assets'
    if not res.is_dir(): raise RuntimeError(f'Decoded resource folder not found: {res}')
    out.mkdir(parents=True,exist_ok=True)
    records=[]
    for xml_path in sorted(res.glob('values*/*.xml')):
        qualifier=xml_path.parent.name
        try: tree=ET.parse(xml_path)
        except ET.ParseError as e: raise RuntimeError(f'Invalid decoded XML {xml_path}: {e}')
        for el in tree.getroot():
            kind=el.tag
            if kind=='item' and el.get('type')=='string': kind='string'
            if kind not in RESOURCE_TAGS: continue
            name=el.get('name')
            if not name: continue
            value=element_value(el,kind)
            records.append({'type':kind,'name':name,'qualifier':qualifier,'source_file':xml_path.relative_to(decoded).as_posix(),'value':value})
    records.sort(key=lambda r:(r['type'],r['name'],r['qualifier'],r['source_file']))
    (out/'resources_catalog.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (out/'resources_catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['type','name','qualifier','source_file','value'])
        w.writeheader()
        for r in records:
            q=dict(r); q['value']=json.dumps(q['value'],ensure_ascii=False) if not isinstance(q['value'],str) else q['value']
            w.writerow(q)
    asset_records=[]; copy_root=out/'text-assets'
    if assets.is_dir():
        for item in sorted(assets.rglob('*')):
            if not item.is_file() or item.suffix.lower() not in TEXT_EXTS: continue
            try: text=item.read_text(encoding='utf-8')
            except UnicodeDecodeError: continue
            rel=item.relative_to(assets).as_posix()
            dest=copy_root/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(item,dest)
            asset_records.append({'path':rel,'chars':len(text),'cjk_characters':len(CJK.findall(text)),'contains_cjk':bool(CJK.search(text))})
    (out/'assets_text_catalog.json').write_text(json.dumps(asset_records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (out/'assets_text_catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['path','chars','cjk_characters','contains_cjk']); w.writeheader(); w.writerows(asset_records)
    print(f'Resource entries exported: {len(records)}')
    print(f'Readable asset files exported: {len(asset_records)}')
    print('Catalog:',out)
if __name__=='__main__': main()
