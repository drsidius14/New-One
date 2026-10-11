# Mi Health Research 1.4.6 ↔ Mi Fitness 3.59.1
## Первичный аудит взаимосвязей и контракт сохранения интеграций

**Статус:** первичный статический анализ; оригинальные APK не изменялись.  
**Назначение:** зафиксировать проверенные точки соприкосновения и обязательные ограничения для последующей русификации.  
**Важно:** наличие строк и объявлений в манифестах подтверждает наличие интеграционных точек, но само по себе не доказывает успешную передачу данных в установленной среде. Для подтверждения полного протокола необходим анализ кода вызовов и динамическая проверка на устройстве.

## 1. Контрольные файлы — неизменяемые эталоны

| Поле | Mi Health Research | Mi Fitness |
|---|---|---|
| Файл | `小米健康研究_1.4.6(1).apk` | `Mi Fitness_3.59.1.apk` |
| Package | `com.mi.healthresearch` | `com.mi.health` |
| Версия | `1.4.6`, versionCode `1004006` | `3.59.1`, versionCode `359001` |
| SHA-256 APK | `9e872f2d75e4ec1d509216d8caa998c2957d797c57b8ecc1ed8c92054f53c4bc` | `46100649d47000e8886d94cfbb34c18706e492a5d3aaa7f34cd4785841ffc254` |
| minSdk / targetSdk | 23 / 33 | 26 / 35 |
| ZIP integrity test | пройден (`testzip=None`) | пройден (`testzip=None`) |
| Подпись, сертификат из META-INF | Xiaomi KeyCenter; SHA-256 `9C:B6:46:2C:D3:15:47:C8:23:76:3E:E8:CA:30:D3:5A:D4:48:F4:03:44:12:CF:6E:6E:E7:7D:FB:52:93:DF:1D` | Xiaomi MIUI; SHA-256 `C9:00:9D:01:EB:F9:F5:D0:30:2B:C7:1B:2F:E9:AA:9A:47:A4:32:BB:A1:73:08:A3:11:1B:75:D7:B2:14:90:25` |

Хеши рассчитаны по фактическим файлам. Хеш Mi Health Research совпадает с эталоном, записанным в `config/project.json` репозитория `drsidius14/New-One`. Сертификаты приложений различаются; это критично при проверке межприложенческих разрешений и доверенных вызовов.

## 2. Подтверждённые точки взаимосвязи

### A. Видимость пакета и разрешения данных

В манифесте Mi Health Research обнаружены:

- `<queries><package android:name="com.mi.health"/></queries>` — объявление видимости пакета Mi Fitness для Android package visibility.
- `uses-permission` для `com.mi.health.permission.DEFAULT_READ_DATA`.
- `uses-permission` для `com.mi.health.permission.DEFAULT_WRITE_DATA`.
- action `mi.intent.action.DEFAULT`.
- экспортируемый сервис `com.xiaomi.fitness.service.DefaultRemoteService` с фильтром action `mi.intent.action.DEFAULT`.

В манифесте Mi Fitness обнаружены:

- собственные объявления разрешений `com.mi.health.permission.DEFAULT_READ_DATA` и `com.mi.health.permission.DEFAULT_WRITE_DATA` с `protectionLevel=0x0` в данном APK.
- экспортируемый сервис `com.xiaomi.fitness.service.DefaultRemoteService`, также связанный с `mi.intent.action.DEFAULT`.
- экспортируемый `DataContentProvider` с authority `com.mi.health.provider.main`.
- экспортируемый `DeviceProvider` с authority `com.mi.health.provider.device`.
- собственное разрешение `com.mi.health.provider.device.read` с `protectionLevel=0x3`.
- строка URI `content://com.mi.health.provider.device/status`.

**Инженерный вывод:** есть явная интеграционная поверхность через package visibility, именованные разрешения, Intent/action, сервисы и ContentProvider. Оба APK объявляют один и тот же сервисный класс и action; нельзя без анализа вызывающего кода предполагать, как приложение разрешает компонент при `bindService`/`startService`. Проверить явный `ComponentName`, `setPackage`, фильтры, Binder-интерфейсы и обработку ошибок.

### B. Общие модели и предметный протокол исследования

В DEX-строках обоих APK присутствуют дескрипторы/имена типов:

- `com.mi.command.data.ResearchApp`
- `com.mi.command.data.SleepEvaluateReminder`
- `com.mi.command.data.HBPMCalibrationRequest`

В Mi Fitness также обнаружены:

- `com.xiaomi.fitness.research.sync.receive.ResearchDataReceiver`
- `com.xiaomi.fitness.research.sync.receive.ResearchDataId`
- `com.xiaomi.fitness.research.export`
- строка `data push to research app , pfd:`
- строка `openHealthResearchApp` и сообщение `openHealthResearchApp failed:`

В Mi Health Research обнаружены:

- `ResearchDataHanderClient init` (именно такое написание в строке APK)
- `research sync device data success`
- `research sync device data error , code:`
- `recordResearchData , researchApp:`
- `updateAppResearch , researchApp:`
- строки `ResearchApp(researchId=`, `SleepEvaluateReminder(researchId=`, `HBPMCalibrationRequest(researchId=`

**Инженерный вывод:** эти совпадения — сильное подтверждение общего протокола исследовательских данных и механизма передачи/синхронизации. Точные поля Parcelable/Serializable, формат Parcel/FileDescriptor (`pfd`), направление каждого метода, Binder descriptor и условия запуска ещё требуется извлечь из декомпилированного кода.

### C. Общий серверный контур

В обоих APK обнаружен домен `hlth.research.xiaomiwear.com` (в Mi Health Research также присутствует staging-домен `staging-hlth.research.xiaomiwear.com`). Это указывает на общий серверный контур исследовательской функции. Нужно сопоставить конкретные API-маршруты, параметры локали, авторизацию, версионирование и структуру payload; сам домен не доказывает, что оба приложения используют одинаковые конечные точки или одинаковую схему данных.

### D. Связь с исследовательскими функциями и устройствами

В Mi Health Research найдены классы/строки, связанные с исследованиями сна, спорта, сердечного ритма и артериального давления, а также операции синхронизации данных с устройством. Mi Fitness содержит Wear Core service, сервисы устройства, экспортируемые провайдеры и исследовательский receiver. Это согласуется с архитектурой, где Mi Fitness выступает источником данных/сервисом устройств, а Mi Health Research потребляет исследовательские данные и открывает исследовательские сценарии. Роль каждого канала должна быть подтверждена трассировкой конкретных вызовов.

## 3. Существенные риски

1. **Разные сертификаты.** Mi Health Research подписан сертификатом Xiaomi KeyCenter, Mi Fitness — сертификатом Xiaomi MIUI. Любая интеграция, которая требует одинаковой подписи или signature-level permission, может перестать работать в модифицированной сборке. Нельзя делать вывод о сохранении такой функции только по успешной компиляции.
2. **Параллельные сервисы с одним action.** В обоих APK есть экспортируемый `com.xiaomi.fitness.service.DefaultRemoteService` и `mi.intent.action.DEFAULT`. Нужно выяснить, как выбирается целевой пакет/компонент; не переименовывать сервисы, action или фильтры.
3. **ContentProvider и authority.** Не менять authority, имена провайдеров, exported/readPermission/writePermission, URI-пути и формат данных.
4. **Binder/Parcel/PFD.** Не менять дескрипторы интерфейсов, имена команд, порядок и типы полей, сериализацию, callbacks, тайм-ауты, жизненный цикл соединения и обработку ошибок.
5. **Серверный API.** Не переводить и не менять домены, URL, query-параметры, имена JSON-полей, ключи, идентификаторы исследований, коды ошибок и протокольные строки.
6. **DEX/native libs.** Не заменять, не удалять и не пересобирать DEX-код или `.so` в рамках локализационного изменения без отдельного доказанного основания и согласования.
7. **Манифест и разрешения.** Не удалять `queries`, uses-permission, custom permission, service/provider/receiver, intent-filter, exported/process/authority атрибуты и не менять package/version без отдельного анализа совместимости.
8. **Не считать одинаковые имена библиотек доказательством идентичности.** Сравнение общих путей `.so` показало, что большинство одноимённых библиотек различаются по SHA-256. Совпадение обнаружено только для `lib/armeabi-v7a/libtensorflowlite_jni.so` среди общих библиотечных путей; для arm64 этой библиотеке хеш не совпал. Никакие библиотеки не переносить между APK.

## 4. Обязательный контракт сохранения интеграций

До любого будущего изменения:

- сохранить оба исходных APK как read-only эталоны и сверять SHA-256;
- по умолчанию не изменять `AndroidManifest.xml`, DEX/smali, нативные библиотеки, имена компонентов, permissions, intent actions, provider authorities, Binder/AIDL/Parcel контракты, URL/API и данные синхронизации;
- локализацию ограничивать ресурсами и текстовыми assets, которые доказанно не участвуют в машинном протоколе;
- при необходимости менять компонент интеграции — сначала представить конкретное основание, риск и план проверки, дождаться согласования;
- отдельно проверять сборку, подпись, установку, запуск, открытие исследовательских экранов, обнаружение Mi Fitness, Binder/service connection, чтение/запись через провайдеры, передачу/синхронизацию исследовательских данных и ошибки при недоступности второго приложения;
- не заявлять, что интеграции сохранены, пока соответствующие сценарии не проверены на устройстве/в поддерживаемой среде;
- изменения в репозиторий передавать только по согласованной схеме ZIP → команды Termux пользователя → чтение GitHub/Actions/артефактов; агент не пишет в GitHub напрямую.

## 5. Ограничения текущего этапа

- Выполнены чтение бинарных AndroidManifest.xml, извлечение строк DEX/assets, сверка хешей и инвентаризация общих библиотечных путей.
- В текущем окружении не обнаружены `jadx`, `apktool`, `aapt2`, `apkanalyzer` и `apksigner`. Поэтому пока нет полноценного Java/Kotlin-декомпилирования, точной таблицы вызовов Binder/ContentResolver, полного декодированного списка компонентов и проверки подписи через apksigner.
- Статический анализ не доказывает фактическую передачу данных в runtime, успешность OAuth/серверной авторизации или работу на конкретной версии Android/MIUI.
- APK не модифицировались; сборки и установка не выполнялись; GitHub не изменялся.

## 6. Следующий этап исследования

1. Подготовить безопасную среду с проверенными версиями JADX/Apktool и Android SDK build-tools, не меняя эталонные APK.
2. Декомпилировать оба APK в отдельные временные каталоги и трассировать все ссылки на `ResearchApp`, `ResearchDataReceiver`, `DefaultRemoteService`, `mi.intent.action.DEFAULT`, `DEFAULT_READ_DATA/WRITE_DATA`, `DataContentProvider`, `DeviceProvider`, `content://com.mi.health.provider.device/status` и домены research.
3. Составить таблицу каналов: инициатор → компонент/метод → формат запроса → формат ответа → permission/signature → ошибки/тайм-ауты → потребляемые данные.
4. Подготовить перечень регрессионных тестов до выбора стратегии русификации.
5. После проверки включить этот отчёт в проект через пользовательский ZIP/Termux workflow; прямой записи в GitHub не выполнять.
