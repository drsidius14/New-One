# APK forensic analysis — Xiaomi Health Research 1.4.6

## Source identity

- Original file: `小米健康研究_1.4.6.apk`
- Original SHA-256: `9e872f2d75e4ec1d509216d8caa998c2957d797c57b8ecc1ed8c92054f53c4bc`
- Package configured in repository: `com.mi.healthresearch`
- Version configured in repository: `1.4.6` / version code `1004006`
- Original Xiaomi signing certificate SHA-256: `9C:B6:46:2C:D3:15:47:C8:23:76:3E:E8:CA:30:D3:5A:D4:48:F4:03:44:12:CF:6E:6E:E7:7D:FB:52:93:DF:1D`
- Original signer subject: `CN=KeyCenter, OU=InfoSec, O=Xiaomi` (self-issued certificate, as provided in the APK)

## Previous CI rebuild — confirmed differences

Comparing the supplied original APK with the APK produced by the previous workflow:

- Original size: `21,494,149` bytes; previous rebuilt APK: `21,736,988` bytes.
- The original uses Xiaomi's certificate; the previous APK uses a CI test certificate with SHA-256 `25:00:6D:37:C8:4A:EF:4E:CA:79:DD:61:D7:48:71:B4:01:97:65:F3:3D:2C:59:01:15:21:D3:03:3B:F2:96:FC`.
- `AndroidManifest.xml` bytes changed.
- `classes.dex` changed from 8,669,600 to 8,677,316 bytes.
- `classes2.dex` changed from 2,924,348 to 2,933,952 bytes.
- `resources.arsc` changed from 1,463,404 to 1,579,268 bytes.
- `assets/questionnaire.html` changed, as intended by an earlier asset override.
- 2,726 original `res/` archive paths were removed and 2,726 different `res/` paths were added; another 174 same-name `res/` entries differed. This is consistent with decoding/rebuilding resource paths rather than a minimal edit to the original APK.
- Native libraries' same-path contents were byte-identical in this comparison, with 13 `.so` files for each of `arm64-v8a` and `armeabi-v7a`.
- At the time of that successful build, `patches/ru/resources.json` on `main` had empty `strings`, `string_arrays`, and `plurals` objects. That success was a technical rebuild, not a Russian localization.

The DEX byte differences do **not by themselves prove** that program behavior changed, but they prove the prior output was not a strict resource-only patch. The changed manifest and signature are independently confirmed.

## Why the screenshots remained Chinese

1. The source resource catalog contained 5,351 resource records, including 1,726 under the default `values` qualifier; the app has no Russian resource set in its supplied APK.
2. The previously built revision had an empty resource patch, so Android had no Russian strings to choose.
3. DEX strings contain hard-coded Xiaomi web-view links with Chinese locale parameters, including `locale=zh_cn` and `lang=zh-CN`, for routes under `watch.iot.mi.com/html/general/index.html`.
4. The privacy/legal screens use remote URLs such as `https://watch.iot.mi.com/html/privacy/index.html?type=research_user_license`. The visible legal body is not present as a local text asset in the extracted asset catalog.
5. The four research-card descriptions from the screenshots were not found as exact static Android string resources in the supplied catalog. They are likely returned by remote data/config or assembled dynamically; runtime text replacements were added for those exact visible strings.

## Corrective decision

Do not rebuild or replace the Xiaomi APK. A valid modified APK requires signing, and Android's signing/update model expects the existing signing key for an update. The Xiaomi certificate does not include Xiaomi's private key, so its signature cannot be recreated. The only path that preserves the original APK signature and its files is an external runtime overlay such as the LSPosed module in this archive, or an official Xiaomi localization/server-side language option.

## Acceptance checklist

- Original `com.mi.healthresearch` APK remains installed and unmodified.
- Module scope is restricted to `com.mi.healthresearch`.
- Static resource replacements match resource names present in the catalog.
- Four dynamic strings match the supplied screenshot text exactly after whitespace normalization.
- No WebView URLs, Intent handoffs, Binder calls, services, PackageManager, or synchronization methods are modified by the current runtime module. Remote legal content therefore remains server-controlled and may remain Chinese.
- Remote legal-document content is not fabricated or silently replaced with an incomplete translation.
- User must verify Russian output and Xiaomi handoffs on the phone; CI compilation alone is insufficient.
