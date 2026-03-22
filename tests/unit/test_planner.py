from __future__ import annotations

import unittest
from pathlib import Path
import sys
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.errors import (
    CircularDependencyError,
    MissingDependencyError,
    UnknownModuleError,
)
from personal_setup.modules import build_module_registry
from personal_setup.models.module import CheckResult, ModuleDefinition
from personal_setup.services.planner import Planner
from personal_setup.services.profile_loader import ProfileLoader
from personal_setup.services.user_settings import UserSettingsStore


class PlannerTest(unittest.TestCase):
    @staticmethod
    def _build_module(name: str, dependencies: tuple[str, ...] = (), ready: bool = False):
        class TestModule:
            definition = ModuleDefinition(
                name=name,
                description=f"{name} module",
                supported_platforms=("windows", "linux"),
                dependencies=dependencies,
            )

            def check(self):
                return CheckResult(
                    name,
                    True,
                    ready,
                    install_required=not ready,
                    details=f"{name} status",
                )

        return TestModule()

    def test_plan_contains_known_modules(self) -> None:
        loader = ProfileLoader(PROJECT_ROOT / "profiles")
        registry = build_module_registry(
            PROJECT_ROOT,
            UserSettingsStore(PROJECT_ROOT / ".local" / "test_user_settings.json"),
        )
        planner = Planner(loader, registry)

        plan = planner.build_plan("full")
        module_names = {step.module_name for step in plan.steps}

        self.assertIn("autohotkey", module_names)
        self.assertIn("git", module_names)
        self.assertIn("glazewm", module_names)
        self.assertIn("project_folders", module_names)
        self.assertIn("neovim", module_names)

    def test_plan_carries_declared_dependencies(self) -> None:
        loader = SimpleNamespace(
            load=lambda _: SimpleNamespace(name="test", modules=("child",))
        )

        planner = Planner(
            loader,
            {
                "base": self._build_module("base"),
                "child": self._build_module("child", dependencies=("base",)),
            },
        )

        plan = planner.build_plan("test")

        self.assertEqual([step.module_name for step in plan.steps], ["base", "child"])
        self.assertEqual(plan.steps[1].dependencies, ("base",))
        self.assertEqual(plan.steps[1].action, "install")

    def test_unknown_module_raises_planning_error(self) -> None:
        loader = SimpleNamespace(
            load=lambda _: SimpleNamespace(name="test", modules=("missing",))
        )
        planner = Planner(loader, {})

        with self.assertRaises(UnknownModuleError):
            planner.build_plan("test")

    def test_missing_dependency_raises_planning_error(self) -> None:
        loader = SimpleNamespace(
            load=lambda _: SimpleNamespace(name="test", modules=("child",))
        )
        planner = Planner(
            loader,
            {"child": self._build_module("child", dependencies=("missing_base",))},
        )

        with self.assertRaises(MissingDependencyError):
            planner.build_plan("test")

    def test_circular_dependency_raises_planning_error(self) -> None:
        loader = SimpleNamespace(
            load=lambda _: SimpleNamespace(name="test", modules=("first",))
        )
        planner = Planner(
            loader,
            {
                "first": self._build_module("first", dependencies=("second",)),
                "second": self._build_module("second", dependencies=("first",)),
            },
        )

        with self.assertRaises(CircularDependencyError):
            planner.build_plan("test")

    def test_repeated_modules_are_deduplicated_in_final_order(self) -> None:
        loader = SimpleNamespace(
            load=lambda _: SimpleNamespace(name="test", modules=("base", "child", "base"))
        )
        planner = Planner(
            loader,
            {
                "base": self._build_module("base"),
                "child": self._build_module("child", dependencies=("base",)),
            },
        )

        plan = planner.build_plan("test")

        self.assertEqual([step.module_name for step in plan.steps], ["base", "child"])


if __name__ == "__main__":
    unittest.main()
