# Mi Health Research — non-invasive Russian overlay

## Why this method

The Xiaomi-signed source APK must remain installed and byte-for-byte unchanged. The previous Apktool rebuild changed the signing certificate and also rewrote `AndroidManifest.xml`, both DEX files and thousands of resource archive paths. That does not meet the project requirements.

This project builds a **separate LSPosed/Xposed runtime module**. It does not replace, resign, patch, or reinstall `com.mi.healthresearch`. It replaces 488 selected Android string resources at runtime and translates exact-match research-card strings when rendered as `TextView` text. It does not alter WebView URLs, cross-app intents, services, Binder calls, or synchronization methods.

## Important requirement

This method requires a rooted Android device with LSPosed (legacy Xposed module support) installed and enabled. Without root/LSPosed, a companion APK cannot transparently replace another app's resources while preserving the original app signature. A standalone repacked APK would have a different signature unless Xiaomi's private signing key were available.

## Coverage and limits

- Includes 488 validated string-resource replacements across common controls, device handoff labels, consent/authentication/profile, heart/blood-pressure/sleep research flows, sleep diary/evaluation, and running-injury risk categories.
- Includes exact text replacements for the four Chinese descriptions shown in the supplied screenshots, plus common dynamic labels.
- Does not modify WebView URLs or remote legal pages because Russian support on Xiaomi servers has not been verified. Remote legal content may remain Chinese; this is deliberate to avoid risking consent/navigation behavior.
- Does not translate an entire remotely delivered legal agreement by guessing its meaning. The legal page's full source and server language support must be verified separately.
- Never changes the target APK's manifest, DEX, native libraries, package ID, signature, network client, intents, permissions, or device integration code.

## Build

A push of this project to `main` triggers `.github/workflows/mihealthresearch-runtime-ru.yml`. The workflow builds and uploads `mihealthresearch-runtime-ru-lsposed.apk` as a GitHub Actions artifact.

## Install

Install the module APK, open LSPosed, enable **Mi Health Research RU**, select scope `com.mi.healthresearch`, then reboot or force-stop/reopen the target app. Keep the original Xiaomi APK installed. Do not uninstall it to try a repacked build.

## Verified vs unverified

The project has a source-level audit and CI build workflow. The Russian runtime substitutions require on-device verification. A green build proves only that the module compiled, not that every screen is translated. Remote legal pages and the Android system dialog that asks to open Mi Fitness are outside the module scope; translating those would require a separate verified approach.
