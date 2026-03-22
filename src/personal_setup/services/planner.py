from __future__ import annotations

from personal_setup.errors import (
    CircularDependencyError,
    MissingDependencyError,
    UnknownModuleError,
)
from personal_setup.models.plan import PlanResult, PlanStep
from personal_setup.platforms.base import detect_platform


class Planner:
    def __init__(self, profile_loader, module_registry) -> None:
        self.profile_loader = profile_loader
        self.module_registry = module_registry

    def build_plan(self, profile_name: str) -> PlanResult:
        platform_name = detect_platform()
        profile = self.profile_loader.load(profile_name)
        steps: list[PlanStep] = []

        ordered_module_names = self._resolve_module_order(profile.modules)

        for module_name in ordered_module_names:
            if module_name not in self.module_registry:
                raise UnknownModuleError(module_name)

            module = self.module_registry[module_name]
            check_result = module.check()

            if check_result.blocked_reason:
                steps.append(
                    PlanStep(
                        module_name,
                        "blocked",
                        check_result.blocked_reason,
                        dependencies=module.definition.dependencies,
                    )
                )
                continue

            if not check_result.applicable:
                steps.append(
                    PlanStep(
                        module_name,
                        "skip",
                        "module not applicable on current platform",
                        dependencies=module.definition.dependencies,
                    )
                )
                continue

            if check_result.ready:
                steps.append(
                    PlanStep(
                        module_name,
                        "keep",
                        "module already satisfies current baseline",
                        dependencies=module.definition.dependencies,
                    )
                )
                continue

            steps.append(
                PlanStep(
                    module_name,
                    check_result.preferred_action,
                    check_result.details or "module needs installation or configuration",
                    dependencies=module.definition.dependencies,
                )
            )

        return PlanResult(profile_name=profile.name, platform_name=platform_name, steps=tuple(steps))

    def _resolve_module_order(self, requested_modules: tuple[str, ...]) -> tuple[str, ...]:
        ordered: list[str] = []
        visited: set[str] = set()
        active_stack: list[str] = []

        for module_name in requested_modules:
            self._visit_module(module_name, visited, active_stack, ordered)

        return tuple(ordered)

    def _visit_module(
        self,
        module_name: str,
        visited: set[str],
        active_stack: list[str],
        ordered: list[str],
    ) -> None:
        if module_name in visited:
            return

        if module_name in active_stack:
            cycle_start = active_stack.index(module_name)
            dependency_chain = tuple(active_stack[cycle_start:] + [module_name])
            raise CircularDependencyError(dependency_chain)

        if module_name not in self.module_registry:
            if active_stack:
                raise MissingDependencyError(active_stack[-1], module_name)
            raise UnknownModuleError(module_name)

        active_stack.append(module_name)
        module = self.module_registry[module_name]

        for dependency_name in module.definition.dependencies:
            self._visit_module(dependency_name, visited, active_stack, ordered)

        active_stack.pop()
        visited.add(module_name)
        ordered.append(module_name)
