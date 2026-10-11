#!/usr/bin/env bash
# Static analysis only: this script does not execute the APK.
set -u
APK="${1:-}"
if [ -z "$APK" ] || [ ! -f "$APK" ]; then
  echo "Usage: bash scripts/analyze-apk.sh /path/to/file.apk" >&2
  return 0 2>/dev/null || :
fi
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS="$ROOT/.tools"
WORK="$ROOT/work/$(basename "$APK" .apk)"
mkdir -p "$WORK"
if command -v sha256sum >/dev/null 2>&1; then sha256sum "$APK" > "$WORK/sha256.txt"; else shasum -a 256 "$APK" > "$WORK/sha256.txt"; fi
command -v aapt >/dev/null 2>&1 && aapt dump badging "$APK" > "$WORK/badging.txt" 2>&1 || :
command -v apkanalyzer >/dev/null 2>&1 && apkanalyzer manifest print "$APK" > "$WORK/manifest-original.xml" 2>&1 || :
if [ -f "$TOOLS/apktool.jar" ]; then
  java -jar "$TOOLS/apktool.jar" d -f "$APK" -o "$WORK/decoded" || echo "Apktool decode failed." >&2
else
  echo "Missing $TOOLS/apktool.jar; run scripts/install-tools.sh." >&2
fi
if [ -x "$TOOLS/jadx/bin/jadx" ]; then
  "$TOOLS/jadx/bin/jadx" -d "$WORK/jadx" "$APK" || echo "JADX failed." >&2
fi
if [ -d "$WORK/decoded/res" ]; then
  python3 "$ROOT/scripts/check-resources.py" "$WORK/decoded/res" > "$WORK/resource-check.txt" 2>&1 || :
fi
printf 'Analysis output: %s\n' "$WORK"
