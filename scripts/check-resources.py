#!/usr/bin/env python3
"""Validate Android resource XML and report likely untranslated CJK text."""
import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="res directory or XML file")
    parser.add_argument("--fail-on-cjk", action="store_true")
    args = parser.parse_args()
    root = args.path
    files = [root] if root.is_file() else sorted(
        p for p in root.rglob("*.xml") if p.is_file()
    ) if root.exists() else []
    if not files:
        print(f"ERROR: no XML files found at {root}", file=sys.stderr)
        return 2
    errors = hits = 0
    for file in files:
        try:
            tree = ET.parse(file)
        except (ET.ParseError, OSError) as exc:
            print(f"XML ERROR: {file}: {exc}")
            errors += 1
            continue
        for elem in tree.iter():
            value = "".join(elem.itertext()).strip()
            if value and CJK.search(value):
                print(f"CJK REVIEW: {file}: <{elem.tag}> name={elem.attrib.get('name','')} text={value[:160]!r}")
                hits += 1
    print(f"Checked {len(files)} XML file(s); XML errors={errors}; CJK candidates={hits}")
    if errors:
        return 1
    if args.fail_on_cjk and hits:
        return 3
    return 0

if __name__ == "__main__":
    sys.exit(main())
