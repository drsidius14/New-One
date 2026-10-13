#!/usr/bin/env python3
"""Fail-closed static identity and integration-contract audit for original Xiaomi APKs."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = Path(os.environ.get("XIAOMI_TEST_REPORT_DIR", str(ROOT / "runtime-report")))
REPORT.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def decode_binary_text(data: bytes) -> str:
    parts = [data.decode("utf-8", "ignore"), data.decode("utf-16le", "ignore"), data.decode("utf-16be", "ignore")]
    return "\n".join(parts)


def fail(message: str) -> None:
    raise RuntimeError(message)


def audit_research_apk() -> dict:
    config = json.loads((ROOT / "config/project.json").read_text(encoding="utf-8"))
    apk = (ROOT / config["base_apk"]).resolve()
    if not apk.is_file():
        fail(f"RESEARCH_APK_MISSING:{apk}")
    actual_hash = sha256(apk)
    expected_hash = config["base_sha256"].lower()
    if actual_hash.lower() != expected_hash:
        fail(f"RESEARCH_APK_SHA256_MISMATCH:expected={expected_hash}:actual={actual_hash}")

    with zipfile.ZipFile(apk) as z:
        bad = z.testzip()
        if bad:
            fail(f"RESEARCH_APK_ZIP_CRC_FAILURE:{bad}")
        names = set(z.namelist())
        for required in ("AndroidManifest.xml", "resources.arsc", "classes.dex"):
            if required not in names:
                fail(f"RESEARCH_APK_REQUIRED_ENTRY_MISSING:{required}")
        manifest = decode_binary_text(z.read("AndroidManifest.xml"))
        dex_names = sorted(n for n in names if n.startswith("classes") and n.endswith(".dex"))
        dex_blob = b"\n".join(z.read(n) for n in dex_names)
        archive_blob = z.read("AndroidManifest.xml") + b"\n" + dex_blob
        archive_text = decode_binary_text(archive_blob)
        libs = sorted(n for n in names if n.startswith("lib/") and n.endswith(".so"))
        abis = sorted({n.split("/")[1] for n in libs if len(n.split("/")) >= 3})

    manifest_contracts = {
        "package_visibility": "com.mi.health",
        "read_permission": "com.mi.health.permission.DEFAULT_READ_DATA",
        "write_permission": "com.mi.health.permission.DEFAULT_WRITE_DATA",
        "default_service": "com.xiaomi.fitness.service.DefaultRemoteService",
        "default_service_action": "mi.intent.action.DEFAULT",
        "jump_activity": "com.xiaomi.fitness.service.JumpActivity",
        "research_splash": "com.mi.research.splash.SplashActivity",
        "research_main": "com.mi.research.main.MainActivity",
        "research_home_action": "com.mi.healthresearch.action.HOME",
        "research_main_action": "com.mi.healthresearch.action.MAIN",
        "auth_activity": "com.mi.research.authHealth.AuthHealthActivity",
    }
    dex_contracts = {
        "target_package": "com.mi.health",
        "device_deeplink": "mihealth://intent?pageType=devicetab",
        "data_pull_year": "pullRecentOneYearFitnessData",
        "data_pull_watermark": "pullFitnessDataByWaterMark",
        "device_data_push": "pushDeviceFitnessData",
        "server_sync": "syncProjectDataWithServer",
        "wearable_package": "com.xiaomi.wearable",
    }
    missing = []
    for label, token in manifest_contracts.items():
        if token not in manifest:
            missing.append(f"manifest:{label}={token}")
    for label, token in dex_contracts.items():
        if token not in archive_text:
            missing.append(f"dex/archive:{label}={token}")
    if missing:
        fail("RESEARCH_INTEGRATION_CONTRACT_MISSING:" + "|".join(missing))
    if "arm64-v8a" not in abis or "armeabi-v7a" not in abis:
        fail(f"RESEARCH_NATIVE_ABI_SET_UNEXPECTED:{abis}")
    if len(libs) != 26:
        fail(f"RESEARCH_NATIVE_LIBRARY_COUNT_UNEXPECTED:expected=26:actual={len(libs)}")

    return {
        "path": str(apk.relative_to(ROOT)),
        "package": config["package_name"],
        "version": config["version_name"],
        "version_code": config["version_code"],
        "sha256": actual_hash,
        "zip_crc": "PASS",
        "manifest_contracts": manifest_contracts,
        "dex_contracts": dex_contracts,
        "native_library_count": len(libs),
        "native_abis": abis,
        "dex_files": dex_names,
    }


def audit_companion_apk() -> dict:
    """Require the exact original Mi Fitness binary for a full two-app runtime test."""
    path = ROOT / "app" / "integration" / "com.mi.health_3.59.1.apk"
    expected = "46100649d47000e8886d94cfbb34c18706e492a5d3aaa7f34cd4785841ffc254"
    if not path.is_file():
        return {
            "status": "BLOCKED_MISSING_ORIGINAL_COMPANION_APK",
            "expected_path": str(path.relative_to(ROOT)),
            "expected_sha256": expected,
            "package": "com.mi.health",
            "version": "3.59.1",
        }
    actual = sha256(path)
    if actual != expected:
        fail(f"MIFITNESS_APK_SHA256_MISMATCH:expected={expected}:actual={actual}")
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            fail(f"MIFITNESS_APK_ZIP_CRC_FAILURE:{bad}")
        names = set(z.namelist())
        if not {"AndroidManifest.xml", "resources.arsc", "classes.dex"}.issubset(names):
            fail("MIFITNESS_APK_REQUIRED_ENTRY_MISSING")
        text = decode_binary_text(z.read("AndroidManifest.xml"))
        blob = decode_binary_text(b"\n".join(z.read(n) for n in names if n.startswith("classes") and n.endswith(".dex")))
        contracts = {
            "jump_activity": "com.xiaomi.fitness.service.JumpActivity",
            "default_service": "com.xiaomi.fitness.service.DefaultRemoteService",
            "default_service_action": "mi.intent.action.DEFAULT",
            "reverse_target_package": "com.mi.healthresearch",
            "reverse_target_activity": "com.mi.research.main.MainActivity",
            "device_schema_activity": "com.xiaomi.fitness.schema.SchemaActivity",
            "deeplink_scheme": "mihealth",
        }
        missing = [f"{k}={v}" for k, v in contracts.items() if v not in (text + "\n" + blob)]
        if missing:
            fail("MIFITNESS_INTEGRATION_CONTRACT_MISSING:" + "|".join(missing))
    return {"status": "PASS", "path": str(path.relative_to(ROOT)), "sha256": actual, "package": "com.mi.health", "version": "3.59.1", "contracts": contracts}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-missing-companion", action="store_true", help="local preflight: pass if Research APK is valid while recording that the Mi Fitness APK is absent")
    args = parser.parse_args()
    report_path = REPORT / "static-contract-report.json"
    try:
        research = audit_research_apk()
        companion = audit_companion_apk()
        report = {
            "status": "PASS" if companion.get("status") == "PASS" else "BLOCKED",
            "research_apk": research,
            "mi_fitness_apk": companion,
            "acceptance_note": "Static Research APK checks passed. Full two-original-APK integration is blocked until the exact original Mi Fitness 3.59.1 APK is placed at app/integration/com.mi.health_3.59.1.apk." if companion.get("status") != "PASS" else "Both original APK identities and integration strings passed static checks.",
        }
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if companion.get("status") == "PASS" or args.allow_missing_companion else 2
    except Exception as exc:
        report = {"status": "FAIL", "error": str(exc)}
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"STATIC_AUDIT_FAIL: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
