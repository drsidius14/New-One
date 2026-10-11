#!/usr/bin/env python3
"""Update the ARM64 emulator workflow directly through GitHub REST API; no git clone needed."""
import base64
import getpass
import json
import os
import sys
import urllib.error
import urllib.request

OWNER = "drsidius14"
REPO = "New-One"
BRANCH = "main"
PATH = ".github/workflows/android-arm64-emulator.yml"
API = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{PATH}"

PUSH_BLOCK = """  push:
    branches:
      - main
    paths:
      - '.github/workflows/android-arm64-emulator.yml'
      - 'scripts/**'
      - 'tests/**'
"""

def request(url, token, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "MiFitness-ARM64-CI-Setup")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    if data is not None:
        req.add_header("Content-Type", "application/json; charset=utf-8")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            details = json.loads(body)
        except Exception:
            details = {"message": body}
        return e.code, details
    except Exception as e:
        return 0, {"message": str(e)}

def main():
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("Нужен GitHub Personal Access Token с правом Contents: Read and write для drsidius14/New-One.")
        print("Токен не сохраняется в файл и не выводится на экран.")
        token = getpass.getpass("Вставь GitHub token (ввод скрыт): ").strip()
    if not token:
        print("Токен не введён; изменений нет.")
        return 2

    status, current = request(API + "?ref=" + BRANCH, token)
    if status != 200:
        print(f"Не удалось прочитать workflow (HTTP {status}): {current.get('message', current)}")
        if status == 401:
            print("Токен неверен или истёк.")
        elif status == 403:
            print("Проверь права токена и доступ к репозиторию.")
        elif status == 404:
            print("Файл или ветка не найдены, либо токен не имеет доступа.")
        return 1

    try:
        original = base64.b64decode(current["content"]).decode("utf-8")
    except Exception as e:
        print(f"Не удалось декодировать файл workflow: {e}")
        return 1

    if not any(line.strip() == "on:" for line in original.splitlines()):
        print("Неожиданная структура workflow: секция on: не найдена. Изменений нет.")
        return 1

    if any(line.startswith("  push:") for line in original.splitlines()):
        print("В workflow уже есть push-триггер. Изменений не требуется.")
        return 0

    lines = original.splitlines(keepends=True)
    idx = next(i for i, line in enumerate(lines) if line.strip() == "on:")
    lines.insert(idx + 1, PUSH_BLOCK)
    updated = "".join(lines)

    if "  push:\n    branches:\n      - main\n" not in updated:
        print("Проверка нового содержимого не прошла. Изменений нет.")
        return 1

    payload = {
        "message": "Run ARM64 emulator CI on relevant pushes",
        "content": base64.b64encode(updated.encode("utf-8")).decode("ascii"),
        "sha": current["sha"],
        "branch": BRANCH
    }
    status, result = request(API, token, method="PUT", payload=payload)
    if status not in (200, 201):
        print(f"GitHub отклонил запись (HTTP {status}): {result.get('message', result)}")
        if status == 403:
            print("Проверь, что токен имеет Contents: Read and write и разрешён для этого репозитория.")
        elif status == 409:
            print("Файл изменился параллельно. Запусти скрипт повторно, чтобы получить актуальную версию.")
        return 1

    commit = result.get("commit", {})
    print("УСПЕХ: workflow напрямую обновлён через GitHub API; локальный клон не нужен.")
    print("Commit:", commit.get("html_url", "(ссылка не вернулась)"))
    print("Actions: https://github.com/drsidius14/New-One/actions")
    print("Открой Actions и пришли мне результат ARM64 emulator workflow.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
