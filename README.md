# New-One — Android APK reverse engineering & localization

Рабочая среда для изучения, декомпиляции, русификации, пересборки и проверки Android APK.

## Состав
- Apktool — ресурсы и AndroidManifest.xml.
- JADX — просмотр декомпилированного Java/Kotlin-кода.
- Android SDK — ADB, aapt2, zipalign, apksigner, apkanalyzer.
- ARM64 Android Emulator workflow — образ `arm64-v8a`, проверка старта и логи.
- Проверки XML и потенциально оставшихся китайских символов.
- GitHub Actions для валидации и ручного smoke-теста ARM64-эмулятора.
- Bootstrap для Termux.

## Быстрый старт в Termux

Из каталога клонированного репозитория:
```bash
pkg update
pkg install -y git curl wget jq python openjdk-17 unzip coreutils
bash scripts/termux-bootstrap.sh
bash scripts/install-tools.sh
```

`aapt`, `apksigner`, `zipalign` и полноценный Android Emulator доступны не во всех средах Termux. Эмулятор Android обычно следует запускать на отдельном компьютере/runner либо тестировать на физическом ARM64-устройстве через ADB.

## Анализ APK
```bash
bash scripts/analyze-apk.sh /path/to/app.apk
python scripts/check-resources.py work/app/decoded/res
```

Декодирование и анализ выполняются статически. APK не запускается скриптами автоматически.

## Сборка
```bash
.tools/apktool b work/app/decoded -o work/app-unsigned.apk
```
Перед установкой тестовой сборки APK необходимо выровнять и подписать. Используйте собственный тестовый keystore вне репозитория. Не коммитьте ключи, пароли, токены или APK, на распространение которых нет разрешения.

## Важно
- APK, подписанный другим сертификатом, обычно нельзя установить поверх оригинала как обновление.
- Поиск CJK-символов — только подсказка для ручной проверки.
- Для критичных работ зафиксируйте проверенные версии инструментов; установка latest не гарантирует совместимость со всеми APK.

Документы: `docs/WORKFLOW.md`, `docs/TOOLS.md`, `docs/SECURITY.md`.
