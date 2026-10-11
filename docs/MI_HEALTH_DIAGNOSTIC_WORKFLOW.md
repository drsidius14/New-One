# Mi Health Research — CI diagnostic workflow

## Purpose

This change repairs the known GitHub-hosted runner failure where Android Emulator's QEMU process cannot load `libpulse.so.0`, and makes diagnostic artifacts available even when boot fails early. It changes CI configuration only; it does not modify either APK, app resources, manifests, DEX, package IDs, permissions, signatures, or integration code.

## What it checks

- Installs Ubuntu 24.04's `libpulse0t64` package and confirms `libpulse.so.0` is visible to the dynamic linker.
- Captures QEMU shared-library dependencies and fails early if `ldd` reports unresolved dependencies.
- Records emulator and ADB versions.
- Boots the configured ARM64 Android system image and verifies `sys.boot_completed`, `ro.product.cpu.abi`, and SDK level.
- Uploads diagnostics in an `always()` step, including emulator logs and host dependency output.

## Run

In GitHub: Actions → ARM64 Android emulator smoke test → Run workflow. Use API level 36 and boot timeout 900 seconds initially. Open the run and download `arm64-emulator-diagnostics` even if the job fails.

## Limits

A successful emulator boot does not prove Mi Fitness integration. This workflow does not install or exercise the two apps; it only establishes a stable emulator and produces useful diagnostics. A separate, explicitly designed integration test must use compatible app builds and check service binding/data exchange. Final acceptance still requires the reported on-device scenario to be retested.

## Expected result

- Emulator infrastructure check: PASS/FAIL, based on actual workflow output.
- Mi Fitness integration: NOT TESTED by this workflow.
