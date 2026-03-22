from __future__ import annotations

import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.services.profile_loader import ProfileLoader
from personal_setup.services.user_settings import UserSettingsStore


class ProfileLoaderTest(unittest.TestCase):
    def test_loads_full_profile(self) -> None:
        loader = ProfileLoader(PROJECT_ROOT / "profiles")

        profile = loader.load("full")

        self.assertEqual(profile.name, "full")
        self.assertIn("autohotkey", profile.modules)
        self.assertIn("git", profile.modules)
        self.assertIn("glazewm", profile.modules)
        self.assertIn("project_folders", profile.modules)
        self.assertIn("neovim", profile.modules)


if __name__ == "__main__":
    unittest.main()
