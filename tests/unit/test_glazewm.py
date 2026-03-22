from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.modules.glazewm import GlazeWMModule


class GlazeWMModuleTest(unittest.TestCase):
    def test_check_requires_config_and_startup_when_installed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            module = GlazeWMModule(
                PROJECT_ROOT,
                config_dir=temp_path / ".glzr" / "glazewm",
                startup_directory=temp_path / "Startup",
                executable_path=temp_path / "glazewm.exe",
                command_exists_fn=lambda _: True,
                winget_available_fn=lambda: True,
                winget_installed_fn=lambda _: True,
            )

            result = module.check()

            self.assertFalse(result.ready)
            self.assertTrue(result.configure_required)
            self.assertEqual(result.preferred_action, "configure")

    def test_apply_copies_config_and_creates_startup_shortcut(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            startup_targets: dict[str, str] = {}

            def fake_create_shortcut(shortcut_path: Path, target_path: Path, arguments: str = ""):
                shortcut_path.parent.mkdir(parents=True, exist_ok=True)
                shortcut_path.write_text("shortcut", encoding="utf-8")
                startup_targets[str(shortcut_path)] = str(target_path)
                return SimpleNamespace(returncode=0)

            def fake_read_shortcut_target(shortcut_path: Path) -> str:
                return startup_targets.get(str(shortcut_path), "")

            executable_path = temp_path / "glazewm.exe"
            executable_path.write_text("exe", encoding="utf-8")

            module = GlazeWMModule(
                PROJECT_ROOT,
                config_dir=temp_path / ".glzr" / "glazewm",
                startup_directory=temp_path / "Startup",
                executable_path=executable_path,
                command_exists_fn=lambda _: True,
                winget_available_fn=lambda: True,
                winget_installed_fn=lambda _: True,
                create_shortcut_fn=fake_create_shortcut,
                read_shortcut_target_fn=fake_read_shortcut_target,
            )

            module.apply()

            self.assertTrue((temp_path / ".glzr" / "glazewm" / "config.yaml").exists())
            self.assertTrue((temp_path / "Startup" / "GlazeWM.lnk").exists())

    def test_check_is_ready_when_config_and_startup_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            startup_targets: dict[str, str] = {}

            def fake_create_shortcut(shortcut_path: Path, target_path: Path, arguments: str = ""):
                shortcut_path.parent.mkdir(parents=True, exist_ok=True)
                shortcut_path.write_text("shortcut", encoding="utf-8")
                startup_targets[str(shortcut_path)] = str(target_path)
                return SimpleNamespace(returncode=0)

            def fake_read_shortcut_target(shortcut_path: Path) -> str:
                return startup_targets.get(str(shortcut_path), "")

            executable_path = temp_path / "glazewm.exe"
            executable_path.write_text("exe", encoding="utf-8")
            module = GlazeWMModule(
                PROJECT_ROOT,
                config_dir=temp_path / ".glzr" / "glazewm",
                startup_directory=temp_path / "Startup",
                executable_path=executable_path,
                command_exists_fn=lambda _: True,
                winget_available_fn=lambda: True,
                winget_installed_fn=lambda _: True,
                create_shortcut_fn=fake_create_shortcut,
                read_shortcut_target_fn=fake_read_shortcut_target,
            )

            module.apply()
            result = module.check()

            self.assertTrue(result.ready)


if __name__ == "__main__":
    unittest.main()
