# Как добавлять переводы

После первого успешного запуска workflow скачайте artifact `mi-health-research-1.4.6-ru-catalog` и откройте `resources_catalog.csv` или JSON. Это фактические ключи, извлечённые из единственного APK в проекте.

В `patches/ru/resources.json` заполняются три словаря. Пример формы:

```json
{
  "strings": {
    "some_existing_key": "Русский текст %1$s"
  },
  "string_arrays": {
    "some_existing_array": ["Первый пункт", "Второй пункт"]
  },
  "plurals": {
    "some_existing_plural": {
      "one": "%d элемент",
      "few": "%d элемента",
      "many": "%d элементов",
      "other": "%d элемента"
    }
  }
}
```

Это только схема примера, **не ключи исходного приложения**. Перед фиксацией используйте реальные названия из каталога. Патчер отклонит неизвестные имена и несовпадение плейсхолдеров.

Текстовый asset заменяется файлом в `patches/ru/assets/overrides/` с тем же относительным путём. Например, `assets/questionnaire.html` патчится файлом `patches/ru/assets/overrides/questionnaire.html`.
