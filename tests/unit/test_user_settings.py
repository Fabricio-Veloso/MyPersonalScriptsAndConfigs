from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.services.user_settings import UserSettingsStore


class UserSettingsStoreTest(unittest.TestCase):
    def test_save_and_load_user_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "user_settings.json"
            store = UserSettingsStore(file_path)

            saved_path = store.save_user_name("Fabricio")

            self.assertEqual(saved_path, file_path)
            self.assertEqual(store.load_user_name(), "Fabricio")


if __name__ == "__main__":
    unittest.main()
