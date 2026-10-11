# Раскладка проекта

| Путь | Назначение |
|---|---|
| `app/base/小米健康研究_1.4.6.apk` | Единственная база, выданная владельцем проекта; не заменять другой версией |
| `app/base/SHA256SUMS` | Проверочная сумма базы |
| `config/project.json` | Идентификатор пакета, версия, SHA-256 и справка о подписи |
| `patches/ru/resources.json` | Переводы Android `string`, `string-array`, `plurals` по фактическим именам ресурсов |
| `patches/ru/assets/overrides/` | Файлы-переопределения для текстовых assets; относительный путь повторяет путь после `assets/` |
| `scripts/verify_source.py` | Проверка строго того исходного APK |
| `scripts/extract_catalog.py` | Каталог ресурсов/текстовых assets в JSON и CSV для перевода |
| `scripts/apply_patch.py` | Вкладывает переводы как values-ru overlay и копирует asset overrides |
| `scripts/validate_patch.py` | Проверка JSON/XML и существования ключей |
| `.github/workflows/mi-health-research-ru-patch.yml` | CI извлечения каталога, применения патчей, сборки и подписи |

Рабочие файлы декомпиляции, сборки и инструменты лежат только в `work/` и `.tools/`, которые исключены из Git.
