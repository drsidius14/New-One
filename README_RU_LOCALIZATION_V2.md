# Mi Health Research RU — localization v2

## Findings from the previous build
- `patches/ru/resources.json` previously had empty `strings`, `string_arrays`, and `plurals` objects.
- Therefore the previous CI job rebuilt and signed an APK without applying Russian translations. A green build was not evidence of localization.
- The supplied screenshots show the first-run consent page and research catalogue remain Chinese.
- The previous APK is signed with a temporary CI key, not Xiaomi's original signing certificate. It cannot be treated as a safe update over the official package. Signature-sensitive Xiaomi ecosystem integrations must be tested explicitly.

## This patch
- Adds a first-pass Russian overlay for 43 existing Android string resources in the exact APK catalog.
- Does not intentionally change package ID, DEX code, native libraries, component declarations, permissions, or intent filters.
- This is not a complete translation. The legal agreement/privacy pages visible in screenshots need source tracing; don't guess legal text or assume the pages are local assets.
- Build, install, screenshot verification, and integration checks are required before calling it ready.

## Integration/signature safety
A rebuilt APK must be re-signed. Without Xiaomi's original private signing key, it will have a different signature. Do not uninstall the official app or overwrite it based on this build. Before distribution, compare the decoded manifest's package/components/permissions/intent filters to the base and test Mi Fitness/Health app handoffs on-device. If Xiaomi enforces same-signature access, resource-only repackaging cannot preserve that trust relationship.

## Apply
Copy `patches/ru/resources.json` into the repository at the same path, commit, and push. The existing workflow should then apply the non-empty resource overlay and publish a new CI APK artifact.
