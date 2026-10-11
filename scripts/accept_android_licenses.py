#!/usr/bin/env python3
"""Accept Android SDK licenses without a fragile `yes | sdkmanager` pipe."""
import shutil
import subprocess
import sys

sdkmanager = shutil.which("sdkmanager")
if not sdkmanager:
    print("ERROR: sdkmanager is not on PATH", file=sys.stderr)
    sys.exit(2)

# Feed many answers through stdin. Unlike `yes | sdkmanager`, this does not
# produce a SIGPIPE/Broken pipe failure when sdkmanager exits early.
answers = (b"y\n" * 100)
try:
    result = subprocess.run(
        [sdkmanager, "--licenses"],
        input=answers,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
except subprocess.TimeoutExpired:
    print("ERROR: sdkmanager --licenses timed out", file=sys.stderr)
    sys.exit(3)

output = result.stdout.decode("utf-8", errors="replace")
print(output[-12000:])
if result.returncode != 0:
    print(f"ERROR: sdkmanager --licenses returned {result.returncode}", file=sys.stderr)
    sys.exit(result.returncode or 4)
print("Android SDK license step completed.")
