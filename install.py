#!/usr/bin/env python3
"""Install the small V550 Agent 3 skill without replacing an existing copy."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "v550-agent-3-minto-memo-coach-student"
SOURCE = ROOT / "skills" / NAME


def main() -> int:
    check = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "verify_package.py")],
        cwd=ROOT, capture_output=True, text=True,
    )
    if check.returncode != 0:
        print("Install stopped: package verification failed.", file=sys.stderr)
        print(check.stdout or check.stderr, file=sys.stderr, end="")
        return 2
    root = Path(os.environ.get("V550_SKILLS_HOME", Path.home() / ".agents" / "skills")).expanduser()
    destination = root / NAME
    if destination.exists() or destination.is_symlink():
        print(f"Install stopped: {destination} already exists. Move it aside or remove it, then rerun.", file=sys.stderr)
        return 1
    root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, destination)
    print(f"Installed {NAME} at {destination}")
    print("Reopen Codex, then invoke $v550-agent-3-minto-memo-coach-student.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
