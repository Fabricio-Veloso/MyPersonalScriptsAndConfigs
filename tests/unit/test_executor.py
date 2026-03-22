from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.models.plan import PlanResult, PlanStep
from personal_setup.services.executor import Executor


class ExecutorTest(unittest.TestCase):
    def test_apply_executes_configure_steps(self) -> None:
        class ConfigurableModule:
            def __init__(self) -> None:
                self.applied = False

            def apply(self) -> None:
                self.applied = True

        module = ConfigurableModule()
        planner = SimpleNamespace(
            build_plan=lambda _: PlanResult(
                profile_name="full",
                platform_name="windows",
                steps=(PlanStep("project_folders", "configure", "needs configuration"),),
            )
        )
        executor = Executor(planner, {"project_folders": module})

        result = executor.apply("full")

        self.assertTrue(module.applied)
        self.assertEqual(result.steps[0].action, "applied")


if __name__ == "__main__":
    unittest.main()
