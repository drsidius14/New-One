#!/usr/bin/env bash
# Best-effort install of official Apktool/JADX releases and Android SDK packages.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS="$ROOT/.tools"
SDK="${ANDROID_HOME:-$HOME/Android/Sdk}"
mkdir -p "$TOOLS" "$SDK"
for cmd in curl jq unzip java; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    printf 'MISSING prerequisite: %s\n' "$cmd" >&2
    printf 'Install it and rerun this script.\n' >&2
    return 0 2>/dev/null || :
  fi
done

fetch_asset() {
  local repo="$1" regex="$2" output="$3" json url tag
  json="$(curl -fsSL "https://api.github.com/repos/$repo/releases/latest")" || return 1
  url="$(printf '%s' "$json" | jq -r --arg re "$regex" '[.assets[] | select(.name | test($re;"i"))][0].browser_download_url // empty')"
  tag="$(printf '%s' "$json" | jq -r '.tag_name // "unknown"')"
  if [ -z "$url" ]; then
    printf 'No matching asset for %s (%s)\n' "$repo" "$tag" >&2
    return 1
  fi
  curl -fL --retry 3 "$url" -o "$output" || return 1
  printf 'Downloaded %s %s\n' "$repo" "$tag"
}
if fetch_asset "iBotPeaches/Apktool" '\.jar$' "$TOOLS/apktool.jar"; then
  printf '#!/usr/bin/env sh\nexec java -jar "%s" "$@"\n' "$TOOLS/apktool.jar" > "$TOOLS/apktool"
  chmod +x "$TOOLS/apktool"
else
  echo "Apktool download failed; inspect official release assets." >&2
fi
if fetch_asset "skylot/jadx" 'jadx-[^/]*\.zip$' "$TOOLS/jadx.zip"; then
  mkdir -p "$TOOLS/jadx"
  unzip -oq "$TOOLS/jadx.zip" -d "$TOOLS/jadx"
else
  echo "JADX download failed; inspect official release assets." >&2
fi

SDKMANAGER="$(command -v sdkmanager 2>/dev/null || true)"
if [ -z "$SDKMANAGER" ] && [ -x "$SDK/cmdline-tools/latest/bin/sdkmanager" ]; then
  SDKMANAGER="$SDK/cmdline-tools/latest/bin/sdkmanager"
fi
if [ -n "$SDKMANAGER" ]; then
  yes | "$SDKMANAGER" --sdk_root="$SDK" --licenses >/dev/null 2>&1 || :
  "$SDKMANAGER" --sdk_root="$SDK" --install "platform-tools" "platforms;android-36" "build-tools;36.0.0" || echo "Some Android SDK packages failed; inspect sdkmanager output." >&2
else
  echo "sdkmanager not found. Install official Android command-line tools, then rerun." >&2
fi
printf 'Tools: %s\nAndroid SDK: %s\n' "$TOOLS" "$SDK"
