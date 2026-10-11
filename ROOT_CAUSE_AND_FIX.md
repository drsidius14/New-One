# Mi Health Research / ARM64 CI — diagnosis

## Verified results
- Commit: `80ec07330657b1beabf4a66876895f3f50c04bff`.
- Russian patch workflow run `38120382416`: SUCCESS. Exact supplied APK verification, tests, Apktool decode, catalog extraction, patch application, build, alignment, signing and artifact upload all completed successfully.
- Artifact `mi-health-research-1.4.6-ru-patched-apk` was downloaded and its ZIP opened successfully. It contains `MiHealthResearch-1.4.6-ru-patched.apk` (21,736,988 bytes).
- ARM64 emulator workflow run `38120382406`: FAILURE. SDK setup and license acceptance succeeded. The job then failed because the shell could not find the `emulator` executable (`emulator: command not found`, exit 127). The preceding `avdmanager` warning about `devices.xml` was logged, but the fatal error was the missing executable on PATH.

## Correction
The replacement workflow adds Android SDK executable directories to `GITHUB_PATH`, resolves `avdmanager` explicitly, and invokes emulator/adb by absolute path. It also retains `emulator.log` upload on failure.

## Limits
This is a proposed correction, not yet validated by a subsequent GitHub Actions run. Do not call the emulator test fixed until a new run passes. The APK was built and signed in CI; successful installation/runtime on a physical phone has not yet been verified.
