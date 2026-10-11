#!/usr/bin/env python3
"""Source and integration-safety checks for the non-invasive runtime module."""
from pathlib import Path
import hashlib
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / "runtime-ru/app/src/main/java/ru/mihealthresearch/runtime/ru/RussianModule.java"
INIT = ROOT / "runtime-ru/app/src/main/assets/xposed_init"
MANIFEST = ROOT / "runtime-ru/app/src/main/AndroidManifest.xml"
GRADLE = ROOT / "runtime-ru/app/build.gradle"
BASE_APK = ROOT / "app/base/小米健康研究_1.4.6.apk"
EXPECTED_BASE_SHA256 = "9e872f2d75e4ec1d509216d8caa998c2957d797c57b8ecc1ed8c92054f53c4bc"
TARGET_PACKAGE = "com.mi.healthresearch"

text = JAVA.read_text(encoding="utf-8")
manifest = MANIFEST.read_text(encoding="utf-8")
gradle = GRADLE.read_text(encoding="utf-8")

assert INIT.read_text(encoding="utf-8").strip() == "ru.mihealthresearch.runtime.ru.RussianModule"
assert f'"{TARGET_PACKAGE}"' in text
assert "IXposedHookInitPackageResources" in text and "IXposedHookLoadPackage" in text
assert 'if (!TARGET_PACKAGE.equals(resparam.packageName)) return;' in text
assert 'if (!TARGET_PACKAGE.equals(lpparam.packageName)) return;' in text
assert "classes.dex" not in text and "AndroidManifest.xml" not in text
assert "RESOURCE_TRANSLATIONS.put" in text
assert "心律失常快速智能筛查" in text
assert "血氧饱和度" in text
assert 'android:name="xposedmodule" android:value="true"' in manifest
assert "applicationId 'ru.mihealthresearch.runtime.ru'" in gradle
assert re.search(r"targetSdk\s+35", gradle), "Companion module must target API 35 for current Android SDK lint requirements."

# Integration safety contract: only user-visible TextView labels may be changed.
hooked = re.findall(r'findAndHookMethod\(TextView\.class, "([^"]+)"', text)
assert hooked and set(hooked) == {"setText"}, f"Unexpected hooked methods: {hooked}"
assert "WebView" not in text and "loadUrl" not in text and "rewriteXiaomiLocaleUrl" not in text, "Remote URLs/content must remain untouched until Russian server support is confirmed."
for forbidden in (
    "com.xiaomi.wearable",
    "com.xiaomi.fitness.service.DefaultRemoteService",
    "com.mi.fitness.ProjectDataCenterRemote",
    "FitnessDataSyncImpl",
    "ProjectDataRecorderImpl",
    "ServiceConnection",
    "IBinder",
    "PackageManager",
    "startActivity(",
    "bindService(",
):
    assert forbidden not in text, f"Localization module must not hook/alter integration component: {forbidden}"

resource_keys = re.findall(r'RESOURCE_TRANSLATIONS\.put\("([^"\\]+)"', text)
coverage_path = ROOT / "patches/ru/runtime-overlay-coverage.json"
coverage = __import__("json").loads(coverage_path.read_text(encoding="utf-8"))
coverage_keys = set(coverage["static_resource_replacements"])
assert len(resource_keys) >= 450, f"Expected >=450 resource translations, got {len(resource_keys)}"
assert len(resource_keys) == len(set(resource_keys)), "Duplicate resource replacement key"
assert set(resource_keys) == coverage_keys, "Java resource replacements and coverage JSON differ"
assert coverage.get("mode") == "runtime overlay; original APK remains byte-identical"
for phrase in ["心脏健康研究", "血压健康研究", "睡眠呼吸暂停研究", "跑步损伤评估", "同意", "不同意并进入基础模式"]:
    assert phrase in text, f"Missing dynamic phrase: {phrase}"

# Hard-pin the original target APK: CI must never substitute or modify it as part of this module.
assert BASE_APK.is_file(), f"Original base APK not found: {BASE_APK}"
sha = hashlib.sha256(BASE_APK.read_bytes()).hexdigest()
assert sha == EXPECTED_BASE_SHA256, f"Unexpected base APK SHA-256: {sha}"
with zipfile.ZipFile(BASE_APK) as apk:
    names = set(apk.namelist())
    assert "AndroidManifest.xml" in names and "classes.dex" in names and "classes2.dex" in names
    libs = sorted(n for n in names if n.endswith(".so"))
    assert len(libs) == 26, f"Unexpected native library inventory: {len(libs)}"

print(f"Source checks passed: {len(resource_keys)} resource replacements; TextView-only hooks; no WebView/Intent/Binder/service hooks; original APK SHA-256 pinned; {len(libs)} native libraries present.")
