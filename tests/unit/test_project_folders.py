from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.modules.project_folders import ProjectFoldersModule
from personal_setup.services.user_settings import UserSettingsStore


class ProjectFoldersModuleTest(unittest.TestCase):
    def test_windows_check_blocks_when_user_name_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            store = UserSettingsStore(temp_path / "user_settings.json")
            module = ProjectFoldersModule(
                PROJECT_ROOT,
                store,
                platform_name="windows",
                windows_root=temp_path,
            )

            result = module.check()

            self.assertEqual(result.status_label, "blocked")
            self.assertTrue(result.configure_required)

    def test_windows_apply_creates_projects_inside_configured_name_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            store = UserSettingsStore(temp_path / "user_settings.json")
            store.save_user_name("Fabricio")
            module = ProjectFoldersModule(
                PROJECT_ROOT,
                store,
                platform_name="windows",
                windows_root=temp_path,
            )

            module.apply()

            self.assertTrue((temp_path / "Fabricio" / "projects").is_dir())

    def test_linux_apply_keeps_projects_inside_current_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            store = UserSettingsStore(temp_path / "user_settings.json")
            store.save_user_name("IgnoredOnLinux")
            module = ProjectFoldersModule(
                PROJECT_ROOT,
                store,
                platform_name="linux",
                linux_home=temp_path,
            )

            module.apply()

            self.assertTrue((temp_path / "projects").is_dir())


if __name__ == "__main__":
    unittest.main()
