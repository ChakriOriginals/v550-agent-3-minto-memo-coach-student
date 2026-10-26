from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "v550-agent-3-minto-memo-coach-student"


class PackageTests(unittest.TestCase):
    def isolated_package(self, temporary: str) -> Path:
        destination = Path(temporary) / "package"
        shutil.copytree(ROOT, destination)
        return destination

    def test_package_verifies(self):
        result = subprocess.run(["python3", str(ROOT / "tools" / "verify_package.py")], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_installs_references_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary) / "skills"
            env = os.environ.copy()
            env["V550_SKILLS_HOME"] = str(home)
            command = ["python3", str(ROOT / "install.py")]
            first = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            installed = home / NAME
            for relative in (
                "SKILL.md", "agents/openai.yaml", "references/Minto_Reference_Sheet.md",
                "references/course-context.md",
            ):
                self.assertEqual(
                    (installed / relative).read_bytes(),
                    (ROOT / "skills" / NAME / relative).read_bytes(),
                )
            marker = installed / "student-note.txt"
            marker.write_text("keep me", encoding="utf-8")
            second = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
            self.assertEqual(second.returncode, 1)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep me")

    def test_installer_rejects_extra_skill_code(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = self.isolated_package(temporary)
            skill = package / "skills" / NAME
            (skill / "tracking.py").write_text("print('unexpected code')\n", encoding="utf-8")
            home = Path(temporary) / "skills-home"
            env = os.environ.copy()
            env["V550_SKILLS_HOME"] = str(home)
            check = subprocess.run(["python3", str(package / "tools" / "verify_package.py")], capture_output=True, text=True)
            install = subprocess.run(["python3", str(package / "install.py")], env=env, capture_output=True, text=True)
            self.assertEqual(check.returncode, 1)
            self.assertIn("Unexpected package file", check.stdout)
            self.assertEqual(install.returncode, 2)
            self.assertFalse((home / NAME).exists())

    def test_installer_rejects_symlinked_reference(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = self.isolated_package(temporary)
            reference = package / "skills" / NAME / "references" / "course-context.md"
            outside = Path(temporary) / "outside.md"
            outside.write_text("external content", encoding="utf-8")
            reference.unlink()
            reference.symlink_to(outside)
            home = Path(temporary) / "skills-home"
            env = os.environ.copy()
            env["V550_SKILLS_HOME"] = str(home)
            check = subprocess.run(["python3", str(package / "tools" / "verify_package.py")], capture_output=True, text=True)
            install = subprocess.run(["python3", str(package / "install.py")], env=env, capture_output=True, text=True)
            self.assertEqual(check.returncode, 1)
            self.assertIn("Symlink is not allowed", check.stdout)
            self.assertEqual(install.returncode, 2)
            self.assertFalse((home / NAME).exists())

    def test_installer_rejects_missing_reference(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = self.isolated_package(temporary)
            (package / "skills" / NAME / "references" / "Minto_Reference_Sheet.md").unlink()
            home = Path(temporary) / "skills-home"
            env = os.environ.copy()
            env["V550_SKILLS_HOME"] = str(home)
            install = subprocess.run(["python3", str(package / "install.py")], env=env, capture_output=True, text=True)
            self.assertEqual(install.returncode, 2)
            self.assertFalse((home / NAME).exists())

    def test_cli_launcher_starts_in_package_folder(self):
        with tempfile.TemporaryDirectory() as temporary:
            fake = Path(temporary) / "codex"
            fake.write_text('#!/bin/sh\nprintf "%s" "$PWD"\n', encoding="utf-8")
            fake.chmod(0o755)
            env = os.environ.copy()
            env["V550_CODEX_CLI"] = str(fake)
            result = subprocess.run(["sh", str(ROOT / "start-v550.sh")], cwd=temporary, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, str(ROOT))

    def test_cli_launcher_rejects_missing_executable(self):
        with tempfile.TemporaryDirectory() as temporary:
            env = os.environ.copy()
            env["V550_CODEX_CLI"] = str(Path(temporary) / "missing-codex")
            result = subprocess.run(["sh", str(ROOT / "start-v550.sh")], cwd=temporary, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("not executable", result.stderr)

    def test_shell_syntax(self):
        result = subprocess.run(["sh", "-n", str(ROOT / "start-v550.sh")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
