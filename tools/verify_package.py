#!/usr/bin/env python3
"""Check the installable package and its deliberately narrow code surface."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "v550-agent-3-minto-memo-coach-student"
FILES = {
    ".gitignore", "README.md", "install.py", "start-v550.sh", "tools/verify_package.py",
    f"skills/{NAME}/SKILL.md", f"skills/{NAME}/agents/openai.yaml",
    f"skills/{NAME}/references/Minto_Reference_Sheet.md",
    f"skills/{NAME}/references/course-context.md",
    "tests/test_package.py", "tests/conversation_checks.md", "tests/synthetic_materials.md",
}
ALLOWED_IMPORTS = {"__future__", "ast", "os", "pathlib", "shutil", "sys", "tempfile", "subprocess", "unittest"}


def main() -> int:
    errors: list[str] = []
    entries = [path for path in ROOT.rglob("*") if ".git" not in path.parts]
    for path in entries:
        if path.is_symlink():
            errors.append(f"Symlink is not allowed: {path.relative_to(ROOT)}")
    actual = {str(path.relative_to(ROOT)) for path in entries if path.is_file() and "__pycache__" not in path.parts}
    for missing in sorted(FILES - actual):
        errors.append(f"Missing: {missing}")
    for unexpected in sorted(actual - FILES):
        errors.append(f"Unexpected package file: {unexpected}")

    for relative in sorted(actual):
        path = ROOT / relative
        if path.name != ".gitignore" and path.suffix not in {".md", ".py", ".sh", ".yaml"}:
            errors.append(f"Unsupported file type: {relative}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Non-text file: {relative}")
            continue
        if path.suffix == ".py":
            try:
                tree = ast.parse(content, filename=relative)
            except SyntaxError as exc:
                errors.append(f"Python syntax: {relative}: {exc}")
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    modules = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    modules = [(node.module or "").split(".")[0]]
                else:
                    continue
                for module in modules:
                    if module not in ALLOWED_IMPORTS:
                        errors.append(f"Unapproved dependency {module}: {relative}")
        if path.suffix in {".py", ".sh"}:
            for fragment in ("http://", "https://", "curl ", "wget ", "requests", "urllib", "socket", "analytics", "telemetry", "scorecard", "readiness", "review_bundle", "transcript"):
                if fragment in content.lower() and path.name != "verify_package.py":
                    errors.append(f"Reporting or gate-related code fragment {fragment!r}: {relative}")

    skill = ROOT / "skills" / NAME / "SKILL.md"
    if skill.is_file() and not skill.read_text(encoding="utf-8").startswith(f"---\nname: {NAME}\n"):
        errors.append("Skill frontmatter name does not match the install folder")
    if errors:
        print("PACKAGE CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PACKAGE CHECK PASSED: {len(actual)} expected text files; no extra code or dependency files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
