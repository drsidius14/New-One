# Xiaomi original APK integration gate

Target repository: `drsidius14/New-One`, branch `main`.

## What the gate checks

1. The Research APK is byte-identical to the pinned original (`config/project.json` SHA-256), its ZIP CRC is valid, required APK entries exist, and its package/version are the configured values.
2. The original Research manifest/DEX still contain the recorded integration contracts: `com.mi.health` package visibility, read/write permission names, `DefaultRemoteService`, `JumpActivity`, the Research exported entry points, `mi.intent.action.DEFAULT`, the `mihealth://intent?pageType=devicetab` route, sync/data method strings and wearable package reference.
3. The original APK has both recorded native ABIs and the expected 26 native `.so` files.
4. On Android 11 / API 30 ARM64 emulator: install and launch the exact original Research APK; collect package/component state, UI hierarchy, screenshot and logcat; install the exact original Mi Fitness APK; resolve the device deep-link and shared service action; check both app entry points and the expected target components. This is a component/contract test; it does not simulate every in-app user tap or prove a live account sync.
5. Always retain machine-readable static report and emulator diagnostics as GitHub Actions artifacts.

## Original companion APK source and identity

The original Mi Fitness 3.59.1 APK is already published as a release asset in this repository's release [`runtime-test-assets-v1`](https://github.com/drsidius14/New-One/releases/tag/runtime-test-assets-v1), under the exact asset name `mi-fitness-3.59.1.apk` (150,579,113 bytes). The workflow downloads this project-owned release asset into a temporary runner workspace; it does not add the 150 MB APK to the Git tree or commit it again.

- Source asset: `https://github.com/drsidius14/New-One/releases/download/runtime-test-assets-v1/mi-fitness-3.59.1.apk`
- Runtime path: `app/integration/com.mi.health_3.59.1.apk` (ephemeral on the runner)
- Package/version: `com.mi.health` / 3.59.1
- Pinned SHA-256: `46100649d47000e8886d94cfbb34c18706e492a5d3aaa7f34cd4785841ffc254`

Each job verifies the downloaded bytes against the pinned SHA-256 before testing. A missing asset, network failure, or hash mismatch fails the job closed. The workflow also checks ZIP CRC and the recorded component/service/deep-link contracts. Static assertions are not a substitute for live Xiaomi account authorization, Bluetooth, wearable-device or server-sync verification.

## Important limits

API 30 is selected because Android emulator ARM64 system images are available for fewer API levels than x86_64 images. A successful emulator run verifies app installation, process startup, component/deep-link/service resolution and the available static contracts. It does not prove Xiaomi account authorization, live server responses, Bluetooth wearables, device sensor data or real-world sync. Those still require the same Xiaomi account and a physical compatible Xiaomi device. A failed ARM emulator startup is recorded as an infrastructure failure, not misreported as an app regression.
