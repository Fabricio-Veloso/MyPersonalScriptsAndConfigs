from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.models.module import CheckResult


class CheckResultTest(unittest.TestCase):
    def test_status_label_for_install_gap(self) -> None:
        result = CheckResult("git", True, False, install_required=True)

        self.assertEqual(result.status_label, "missing-install")
        self.assertEqual(result.preferred_action, "install")

    def test_status_label_for_config_gap(self) -> None:
        result = CheckResult("glazewm", True, False, configure_required=True)

        self.assertEqual(result.status_label, "missing-config")
        self.assertEqual(result.preferred_action, "configure")

    def test_status_label_for_full_ready_state(self) -> None:
        result = CheckResult("git", True, True)

        self.assertEqual(result.status_label, "ready")
        self.assertEqual(result.preferred_action, "keep")


if __name__ == "__main__":
    unittest.main()
