ПАКЕТ: MiHealthResearch_RU_IntegrationSafe_v4.zip
ЦЕЛЬ: исправить сборку отдельного LSPosed-модуля и добавить автоматические проверки неприкосновенности интеграции.
Оригинальный APK не заменяется и не переподписывается. В модуле 488 статических замен; hook-и ограничены TextView. WebView URL, Intent, Binder, сервисы и синхронизация не перехватываются.

1. Скачай ZIP в Download телефона.
2. Открой Termux и выполни блок целиком в каталоге клона drsidius14/New-One.

cd ~/Mihealthreserch
pkg install -y unzip python git gh
unzip -o ~/storage/shared/Download/MiHealthResearch_RU_IntegrationSafe_v4.zip -d .
python3 tools/verify_runtime_module.py
git diff --check
git status --short
git add runtime-ru/app/build.gradle runtime-ru/app/src/main/java/ru/mihealthresearch/runtime/ru/RussianModule.java tools/verify_runtime_module.py patches/ru/runtime-overlay-coverage.json README_RU.md docs/FORENSIC_ANALYSIS.md docs/MI_FITNESS_INTEGRATION_AUDIT_RU.md .github/workflows/mihealthresearch-runtime-ru.yml docs/TERMUX_UPLOAD_V4.md
git commit -m "Expand Russian runtime UI and protect Mi Fitness integration"
git push origin main
gh run list --repo drsidius14/New-One --limit 5

ВАЖНО: это отдельный LSPosed-модуль, а не пересобранный Mi Health Research. Для его работы требуются root и LSPosed. Если root/LSPosed нет, модуль не активируется; оригинальный APK всё равно остаётся нетронутым. Русский текст юридических WebView-страниц и системного диалога Android о запуске Mi Fitness не гарантируется.

ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:
- Локальные проверки проходят и подтверждают SHA-256 исходного Xiaomi APK.
- GitHub Actions пытается собрать отдельный runtime overlay APK.
- После push нужно проверить conclusion у нового workflow. Только при успехе скачивается artifact `mihealthresearch-runtime-ru-lsposed`.
- Установка модуля требует root + LSPosed и включения scope `com.mi.healthresearch`; Xiaomi APK остаётся установленным без изменений.

Если `cd ~/Mihealthreserch` не существует, сначала перейдите в фактическую папку уже клонированного репозитория `drsidius14/New-One`; остальные команды выполняются там. Не удаляй и не переустанавливай оригинальный Mi Health Research ради этой сборки.
