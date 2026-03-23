from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.models.module import CheckResult
from personal_setup.services.verifier import Verifier


class VerifierTest(unittest.TestCase):
    def test_verify_passes_sandbox_flag_to_modules(self) -> None:
        captured: list[bool] = []

        class FakeModule:
            def verify(self, *, sandbox: bool = False):
                captured.append(sandbox)
                return CheckResult("neovim", True, True, details="ok")

        verifier = Verifier(
            SimpleNamespace(load=lambda _: SimpleNamespace(name="full", modules=("neovim",))),
            {"neovim": FakeModule()},
        )

        result = verifier.verify("full", sandbox=True)

        self.assertEqual(captured, [True])
        self.assertEqual(result.steps[0].action, "verified")


if __name__ == "__main__":
    unittest.main()
