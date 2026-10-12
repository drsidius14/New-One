#!/data/data/com.termux/files/usr/bin/bash
# Uploads only the two agreed files through GitHub REST API. No git clone/init/repository copy.
set -Eeuo pipefail

REPO="drsidius14/New-One"
BRANCH="main"
ZIP_PATH="${1:-$HOME/storage/downloads/MI_HEALTH_INTEGRATION_DIAGNOSTICS_V3.zip}"
if [ ! -f "$ZIP_PATH" ] && [ -f "/storage/emulated/0/Download/MI_HEALTH_INTEGRATION_DIAGNOSTICS_V3.zip" ]; then ZIP_PATH="/storage/emulated/0/Download/MI_HEALTH_INTEGRATION_DIAGNOSTICS_V3.zip"; fi
TMP_DIR="$(mktemp -d)"

finish() {
  rc=$?
  rm -rf "$TMP_DIR"
  echo
  if [ "$rc" -eq 0 ]; then
    echo "Статус: загрузка файлов в GitHub завершена. Проверьте GitHub Actions."
  else
    echo "ОШИБКА: код $rc. Подробности выше; ничего не скрыто."
  fi
  read -r -p "Нажмите Enter, чтобы завершить скрипт (терминал останется открытым)... " _ || true
  return "$rc"
}
trap finish EXIT

command -v gh >/dev/null || { echo "Не найден GitHub CLI (gh). Установите его в Termux: pkg install gh"; false; }
command -v jq >/dev/null || { echo "Не найден jq. Установите: pkg install jq"; false; }
gh auth status
[ -f "$ZIP_PATH" ] || { echo "ZIP не найден: $ZIP_PATH. Передайте путь к ZIP первым аргументом."; false; }
unzip -q "$ZIP_PATH" -d "$TMP_DIR"
WF="$TMP_DIR/.github/workflows/mi-health-integration-diagnostics.yml"
HELPER="$TMP_DIR/scripts/mi_health_integration_diagnostics.sh"
[ -f "$WF" ] && [ -f "$HELPER" ] || { echo "В ZIP отсутствуют ожидаемые файлы."; false; }

upload_file() {
  local src="$1" dest="$2" message="$3" current_sha=""
  local encoded
  encoded="$(base64 < "$src" | tr -d '\n')"
  if current_sha="$(gh api "repos/$REPO/contents/$dest?ref=$BRANCH" --jq '.sha' 2>/dev/null)"; then
    gh api --method PUT "repos/$REPO/contents/$dest" \
      -f message="$message" -f branch="$BRANCH" -f sha="$current_sha" -f content="$encoded" \
      --jq '"updated: " + .content.path + " @ " + .commit.sha'
  else
    gh api --method PUT "repos/$REPO/contents/$dest" \
      -f message="$message" -f branch="$BRANCH" -f content="$encoded" \
      --jq '"created: " + .content.path + " @ " + .commit.sha'
  fi
}

echo "Цель: https://github.com/$REPO/tree/$BRANCH"
echo "Передача двух файлов через GitHub API; локальный Git-репозиторий не создаётся."
upload_file "$WF" ".github/workflows/mi-health-integration-diagnostics.yml" "Add Mi Health integration diagnostics workflow"
upload_file "$HELPER" "scripts/mi_health_integration_diagnostics.sh" "Add Mi Health diagnostics helper"
echo
echo "Проверяю наличие workflow в целевой ветке..."
gh api "repos/$REPO/contents/.github/workflows/mi-health-integration-diagnostics.yml?ref=$BRANCH" --jq '"Workflow confirmed: " + .path'
echo "Откройте: https://github.com/$REPO/actions/workflows/mi-health-integration-diagnostics.yml"
