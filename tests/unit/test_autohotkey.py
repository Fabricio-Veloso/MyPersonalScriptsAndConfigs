from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.modules.autohotkey import AutoHotkeyModule


class AutoHotkeyModuleTest(unittest.TestCase):
    def test_check_requires_install_and_config_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            documents_dir = Path(temp_dir)
            module = AutoHotkeyModule(
                PROJECT_ROOT,
                documents_dir=documents_dir,
                command_exists_fn=lambda _: False,
                winget_available_fn=lambda: True,
                winget_installed_fn=lambda _: False,
            )

            result = module.check()

            self.assertTrue(result.install_required)
            self.assertTrue(result.configure_required)
            self.assertEqual(result.preferred_action, "install")

    def test_check_blocks_when_winget_is_missing_and_install_is_needed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            documents_dir = Path(temp_dir)
            module = AutoHotkeyModule(
                PROJECT_ROOT,
                documents_dir=documents_dir,
                command_exists_fn=lambda _: False,
                winget_available_fn=lambda: False,
                winget_installed_fn=lambda _: False,
            )

            result = module.check()

            self.assertEqual(result.status_label, "blocked")

    def test_apply_installs_and_copies_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            documents_dir = Path(temp_dir) / "Documents"
            install_calls: list[str] = []

            module = AutoHotkeyModule(
                PROJECT_ROOT,
                documents_dir=documents_dir,
                command_exists_fn=lambda _: False,
                winget_available_fn=lambda: True,
                winget_installed_fn=lambda _: False,
                winget_install_fn=lambda package_id: install_calls.append(package_id) or SimpleNamespace(returncode=0),
            )

            module.apply()

            self.assertEqual(install_calls, ["AutoHotkey.AutoHotkey"])
            self.assertTrue((documents_dir / "AutoHotkey" / "main.ahk").exists())

    def test_apply_only_copies_config_when_already_installed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            documents_dir = Path(temp_dir) / "Documents"
            install_calls: list[str] = []

            module = AutoHotkeyModule(
                PROJECT_ROOT,
                documents_dir=documents_dir,
                command_exists_fn=lambda _: True,
                winget_available_fn=lambda: True,
                winget_installed_fn=lambda _: True,
                winget_install_fn=lambda package_id: install_calls.append(package_id) or SimpleNamespace(returncode=0),
            )

            module.apply()

            self.assertEqual(install_calls, [])
            self.assertTrue((documents_dir / "AutoHotkey" / "main.ahk").exists())

    def test_apply_tolerates_non_zero_winget_when_binary_becomes_available(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            documents_dir = Path(temp_dir) / "Documents"
            install_state = {"installed": False}

            def fake_command_exists(_: str) -> bool:
                return install_state["installed"]

            def fake_install(_: str):
                install_state["installed"] = True
                return SimpleNamespace(returncode=1, stdout="already installed", stderr="")

            module = AutoHotkeyModule(
                PROJECT_ROOT,
                documents_dir=documents_dir,
                command_exists_fn=fake_command_exists,
                winget_available_fn=lambda: True,
                winget_installed_fn=lambda _: install_state["installed"],
                winget_install_fn=fake_install,
            )

            module.apply()

            self.assertTrue((documents_dir / "AutoHotkey" / "main.ahk").exists())

    def test_check_uses_winget_presence_when_executable_is_not_in_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            documents_dir = Path(temp_dir)
            startup_dir = Path(temp_dir) / "Startup"
            (documents_dir / "AutoHotkey").mkdir(parents=True, exist_ok=True)
            (documents_dir / "AutoHotkey" / "main.ahk").write_text("test", encoding="utf-8")
            startup_dir.mkdir(parents=True, exist_ok=True)
            (startup_dir / "mainScript.ahk").write_text("test", encoding="utf-8")
            module = AutoHotkeyModule(
                PROJECT_ROOT,
                documents_dir=documents_dir,
                startup_directory=startup_dir,
                command_exists_fn=lambda _: False,
                winget_available_fn=lambda: True,
                winget_installed_fn=lambda _: True,
                files_match_fn=lambda source, destination: destination.exists(),
            )

            result = module.check()

            self.assertTrue(result.ready)


if __name__ == "__main__":
    unittest.main()
