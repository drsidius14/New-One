#!/data/data/com.termux/files/usr/bin/bash
# Best-effort Termux bootstrap. Does not close the shell.
set -u
pkg update
pkg install -y git curl wget jq python openjdk-17 unzip coreutils
for tool in java curl jq python; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf 'OK: %s -> %s\n' "$tool" "$(command -v "$tool")"
  else
    printf 'MISSING: %s\n' "$tool"
  fi
done
echo
echo "Termux on ARM64 is suitable for local analysis; a full Android Emulator usually needs a separate supported host."
echo "From the repository root, run: bash scripts/install-tools.sh"
echo "SDK emulator images are not installed by this script because host virtualization support is required."
