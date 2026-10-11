# Mi Health Research workflow repair

This archive repairs the Android SDK setup and license acceptance steps in two workflows.

## Files
- `.github/workflows/mi-health-research-ru-patch.yml` — stable major versions of GitHub Actions; accepts licenses before installing Build Tools; verifies `zipalign` and `apksigner`.
- `.github/workflows/android-arm64-emulator.yml` — upgrades Android SDK setup and verifies the ARM64 image prerequisites.
- `scripts/accept_android_licenses.py` — avoids the `yes: Broken pipe` failure caused by a shell pipeline under `pipefail`.

## Safety
The patch does not include or replace the APK. It keeps the configured source APK and its SHA-256 guard unchanged.
After applying, inspect Git diff and let GitHub Actions confirm the actual result. No workflow repair can guarantee all runner/network failures in advance.
