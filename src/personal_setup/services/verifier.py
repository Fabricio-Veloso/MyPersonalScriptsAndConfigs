from __future__ import annotations

from personal_setup.models.plan import PlanResult, PlanStep
from personal_setup.platforms.base import detect_platform


class Verifier:
    def __init__(self, profile_loader, module_registry) -> None:
        self.profile_loader = profile_loader
        self.module_registry = module_registry

    def verify(self, profile_name: str, *, sandbox: bool = False) -> PlanResult:
        platform_name = detect_platform()
        profile = self.profile_loader.load(profile_name)
        steps: list[PlanStep] = []

        for module_name in profile.modules:
            result = self.module_registry[module_name].verify(sandbox=sandbox)
            action = "verified" if result.ready else "failed"
            steps.append(PlanStep(module_name, action, result.details or result.status_label))

        return PlanResult(profile.name, platform_name, tuple(steps))
