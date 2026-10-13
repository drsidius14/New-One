#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPORT="$ROOT/runtime-report"
mkdir -p "$REPORT"
APK="$ROOT/app/base/小米健康研究_1.4.6.apk"
FITNESS_APK="$ROOT/app/integration/com.mi.health_3.59.1.apk"
LOGCAT="$REPORT/logcat-full.txt"
STATUS=0

run() {
  local label="$1"; shift
  echo "===== $label =====" | tee -a "$REPORT/emulator-test.log"
  "$@" 2>&1 | tee -a "$REPORT/emulator-test.log"
  local rc=${PIPESTATUS[0]}
  echo "RESULT $label rc=$rc" | tee -a "$REPORT/emulator-test.log"
  if [ "$rc" -ne 0 ]; then STATUS=1; fi
  return 0
}

{
  echo "UTC_START=$(date -u +%FT%TZ)"
  echo "ANDROID_SERIAL=${ANDROID_SERIAL:-emulator-5554}"
  adb devices -l
  adb shell getprop ro.build.version.release
  adb shell getprop ro.build.version.sdk
  adb shell getprop ro.product.cpu.abilist
} > "$REPORT/emulator-environment.txt" 2>&1

python3 "$ROOT/tests/integration/verify_original_apks.py" > "$REPORT/static-audit-in-emulator.log" 2>&1
STATIC_RC=$?
cat "$REPORT/static-audit-in-emulator.log"
if [ "$STATIC_RC" -ne 0 ]; then
  echo "STATIC_AUDIT_RC=$STATIC_RC" >> "$REPORT/emulator-test.log"
  STATUS=1
fi

# The emulator must support the original APK's ARM ABIs; do not install an ABI-incompatible build.
DEVICE_ABIS="$(adb shell getprop ro.product.cpu.abilist | tr -d '\r')"
if ! printf '%s' "$DEVICE_ABIS" | grep -Eq 'arm64-v8a|armeabi-v7a'; then
  echo "BLOCKED_EMULATOR_ABI: device ABI list '$DEVICE_ABIS' has no ARM ABI required by the original APK" | tee -a "$REPORT/emulator-test.log"
  STATUS=1
else
  run "Install exact original Research APK" adb install -r "$APK"
  run "Confirm Research package installed" adb shell pm path com.mi.healthresearch
  run "Dump Research package/component declarations" adb shell dumpsys package com.mi.healthresearch
  run "Launch exported Research MainActivity" adb shell am start -W -n com.mi.healthresearch/com.mi.research.main.MainActivity
  sleep 12
  run "Capture Research process state" adb shell dumpsys activity activities
  run "Capture UI hierarchy" adb shell uiautomator dump /sdcard/window.xml
  adb pull /sdcard/window.xml "$REPORT/research-window.xml" >> "$REPORT/emulator-test.log" 2>&1 || true
  adb exec-out screencap -p > "$REPORT/research-screen.png" 2>> "$REPORT/emulator-test.log" || true
  adb logcat -d -v threadtime > "$LOGCAT" 2>&1 || true
  grep -E 'FATAL EXCEPTION|AndroidRuntime|UnsatisfiedLinkError|SecurityException|com\.mi\.healthresearch' "$LOGCAT" > "$REPORT/relevant-logcat.txt" || true
  if grep -Eq 'FATAL EXCEPTION|UnsatisfiedLinkError' "$REPORT/relevant-logcat.txt"; then
    echo "CRASH_OR_NATIVE_LOAD_FAILURE detected; inspect relevant-logcat.txt" | tee -a "$REPORT/emulator-test.log"
    STATUS=1
  fi
fi

if [ -f "$FITNESS_APK" ]; then
  run "Install exact original Mi Fitness APK" adb install -r "$FITNESS_APK"
  run "Confirm Mi Fitness package installed" adb shell pm path com.mi.health
  run "Resolve Mi Fitness device deep-link route" adb shell cmd package query-activities --brief --components -a android.intent.action.VIEW -d 'mihealth://intent?pageType=devicetab' -p com.mi.health
  run "Resolve Research default service action" adb shell cmd package query-services --brief --components -a mi.intent.action.DEFAULT -p com.mi.healthresearch
  run "Resolve Mi Fitness default service action" adb shell cmd package query-services --brief --components -a mi.intent.action.DEFAULT -p com.mi.health
  run "Launch Mi Fitness JumpActivity" adb shell am start -W -n com.mi.health/com.xiaomi.fitness.service.JumpActivity
  run "Confirm reverse-target Research MainActivity is launchable" adb shell am start -W -n com.mi.healthresearch/com.mi.research.main.MainActivity
  adb logcat -d -v threadtime > "$REPORT/logcat-two-apps.txt" 2>&1 || true
else
  echo "BLOCKED_TWO_APP_RUNTIME: missing app/integration/com.mi.health_3.59.1.apk; no substitute/fake companion APK will be generated." | tee -a "$REPORT/emulator-test.log"
  STATUS=1
fi

{
  echo "UTC_END=$(date -u +%FT%TZ)"
  echo "FINAL_STATUS=$STATUS"
} | tee -a "$REPORT/emulator-test.log"
exit "$STATUS"
