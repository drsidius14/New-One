# Termux upload commands

Put `MiHealthResearch_NonInvasive_RU_Module.zip` in the phone's `Download` folder. Run the commands below in the clone directory already used for `drsidius14/New-One`.

```bash
cd ~/New-One-fix-20261011-100810
pkg install -y unzip python git gh
unzip -o ~/storage/shared/Download/MiHealthResearch_NonInvasive_RU_Module.zip
python3 tools/verify_runtime_module.py
git diff --check
git add .github/workflows/mihealthresearch-runtime-ru.yml runtime-ru tools/verify_runtime_module.py docs/FORENSIC_ANALYSIS.md docs/TERMUX_UPLOAD.md README_RU.md
git commit -m "Add non-invasive Russian runtime overlay"
git push origin main
gh run list --repo drsidius14/New-One --limit 5
```

This push builds the companion **LSPosed module APK**, not a replacement for Xiaomi's original APK. The original APK is never overwritten or re-signed.
