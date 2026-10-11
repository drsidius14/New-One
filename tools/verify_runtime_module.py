#!/usr/bin/env python3
"""Source-level checks for the non-invasive runtime localization module."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / "runtime-ru/app/src/main/java/ru/mihealthresearch/runtime/ru/RussianModule.java"
INIT = ROOT / "runtime-ru/app/src/main/assets/xposed_init"
MANIFEST = ROOT / "runtime-ru/app/src/main/AndroidManifest.xml"
text = JAVA.read_text(encoding="utf-8")
manifest = MANIFEST.read_text(encoding="utf-8")
assert INIT.read_text(encoding="utf-8").strip() == "ru.mihealthresearch.runtime.ru.RussianModule"
assert '"com.mi.healthresearch"' in text
assert "IXposedHookInitPackageResources" in text and "IXposedHookLoadPackage" in text
assert "classes.dex" not in text and "AndroidManifest.xml" not in text
assert "locale=zh_cn" in text and "locale=ru_ru" in text
assert "RESOURCE_TRANSLATIONS.put" in text
assert "心律失常快速智能筛查" in text
assert "血氧饱和度" in text
assert 'android:name="xposedmodule" android:value="true"' in manifest
resource_keys = re.findall(r'RESOURCE_TRANSLATIONS\.put\("([^"]+)",', text)
assert len(resource_keys) >= 60, f"Expected >=60 resource translations, got {len(resource_keys)}"
assert len(resource_keys) == len(set(resource_keys)), "Duplicate resource replacement key"
for phrase in ["心脏健康研究", "血压健康研究", "睡眠呼吸暂停研究", "跑步损伤评估", "同意", "不同意并进入基础模式"]:
    assert phrase in text, f"Missing dynamic phrase: {phrase}"
print(f"Source checks passed: {len(resource_keys)} resource replacements; dynamic strings and URL locale rewrite present.")
