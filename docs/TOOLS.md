# Закреплённые инструменты и действия CI

- **Apktool 3.0.3** — официальный релиз: https://github.com/iBotPeaches/Apktool/releases/tag/v3.0.3
- **SHA-256 Apktool 3.0.3 JAR** — `dbf930b076c6b9be08d57c449cacefc3bdd6b71ebd59b3066fc0e1f5b14f9423`; workflow сверяет сумму до запуска. Контрольная сумма опубликована в заметках релиза: https://apktool.org/blog/apktool-3.0.3/
- CI использует GitHub Actions `checkout@v7`, `setup-java@v6`, `setup-android@v4` и `upload-artifact@v7`.
- Воспроизводимость обеспечивается фиксацией исходного APK по SHA-256 и закреплённой версией Apktool. CI-ключ создаётся только для текущего запуска и удаляется после подписи.

Apktool и Actions скачиваются из официальных источников во время запуска. Бинарники инструментов не копируются в репозиторий.
