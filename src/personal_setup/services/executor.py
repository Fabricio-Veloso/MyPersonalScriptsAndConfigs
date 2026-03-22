from __future__ import annotations

from personal_setup.models.plan import PlanResult, PlanStep


class Executor:
    def __init__(self, planner, module_registry) -> None:
        self.planner = planner
        self.module_registry = module_registry

    def apply(self, profile_name: str) -> PlanResult:
        plan = self.planner.build_plan(profile_name)
        applied_steps: list[PlanStep] = []

        for step in plan.steps:
            if step.action not in {"apply", "install", "configure"}:
                applied_steps.append(step)
                continue

            module = self.module_registry[step.module_name]
            module.apply()
            applied_steps.append(
                PlanStep(
                    step.module_name,
                    "applied",
                    f"{step.action} workflow executed",
                    dependencies=step.dependencies,
                )
            )

        return PlanResult(plan.profile_name, plan.platform_name, tuple(applied_steps))
