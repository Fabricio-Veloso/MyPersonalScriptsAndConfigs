from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.cli import run_interactive_menu


class CliMenuTest(unittest.TestCase):
    def test_interactive_menu_configures_user_and_exits(self) -> None:
        class FakeApp:
            def __init__(self) -> None:
                self.saved_name = None

            def configure_user_name(self, user_name: str):
                self.saved_name = user_name
                return PROJECT_ROOT / ".local" / "user_settings.json"

        app = FakeApp()
        output = io.StringIO()

        with redirect_stdout(output):
            with patch("builtins.input", side_effect=["1", "Fabricio", "0"]):
                exit_code = run_interactive_menu(app)

        self.assertEqual(exit_code, 0)
        self.assertEqual(app.saved_name, "Fabricio")
        self.assertIn("Configure user", output.getvalue())

    def test_interactive_menu_handles_apply_error_without_crashing(self) -> None:
        class FakeApp:
            def apply(self, _profile_name: str):
                raise RuntimeError("boom")

        app = FakeApp()
        output = io.StringIO()

        with redirect_stdout(output):
            with patch("builtins.input", side_effect=["3", "0"]):
                exit_code = run_interactive_menu(app)

        self.assertEqual(exit_code, 0)
        self.assertIn("Erro ao executar apply: boom", output.getvalue())


if __name__ == "__main__":
    unittest.main()
