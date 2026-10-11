# Mi Health Research — non-invasive Russian overlay

## Why this method

The Xiaomi-signed source APK must remain installed and byte-for-byte unchanged. The previous Apktool rebuild changed the signing certificate and also rewrote `AndroidManifest.xml`, both DEX files and thousands of resource archive paths. That does not meet the project requirements.

This project builds a **separate LSPosed/Xposed runtime module**. It does not replace, resign, patch, or reinstall `com.mi.healthresearch`. It replaces selected Android string resources at runtime, translates four exact server-delivered research-card descriptions when they are rendered as `TextView` text, and changes hard-coded Xiaomi web-view locale parameters from Chinese to Russian.

## Important requirement

This method requires a rooted Android device with LSPosed (legacy Xposed module support) installed and enabled. Without root/LSPosed, a companion APK cannot transparently replace another app's resources while preserving the original app signature. A standalone repacked APK would have a different signature unless Xiaomi's private signing key were available.

## Coverage and limits

- Includes Russian for the primary screen, onboarding labels and selected research labels.
- Includes exact text replacements for the four Chinese descriptions shown in the supplied screenshots.
- Changes `locale=zh_cn` / `lang=zh-CN` parameters on the identified Xiaomi legal/research WebView URLs to `locale=ru_ru` / `lang=ru-RU`. Whether Xiaomi's server actually provides Russian is not yet verified. If its server does not have Russian content, that page can remain Chinese; the hook does not falsify or rewrite legal-document body text.
- Does not translate an entire remotely delivered legal agreement by guessing its meaning. The legal page's full source and server language support must be verified separately.
- Never changes the target APK's manifest, DEX, native libraries, package ID, signature, network client, intents, permissions, or device integration code.

## Build

A push of this project to `main` triggers `.github/workflows/mihealthresearch-runtime-ru.yml`. The workflow builds and uploads `mihealthresearch-runtime-ru-lsposed.apk` as a GitHub Actions artifact.

## Install

Install the module APK, open LSPosed, enable **Mi Health Research RU**, select scope `com.mi.healthresearch`, then reboot or force-stop/reopen the target app. Keep the original Xiaomi APK installed. Do not uninstall it to try a repacked build.

## Verified vs unverified

The project has a source-level audit and CI build workflow. The Russian runtime substitutions and server locale fallback still require on-device verification. A green build proves that the module compiled; it does not prove that the remote Xiaomi site supports `ru_ru` or that every app screen is translated.
