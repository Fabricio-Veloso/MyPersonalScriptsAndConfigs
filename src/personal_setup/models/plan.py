from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PlanStep:
    module_name: str
    action: str
    reason: str
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    blocked_by: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PlanResult:
    profile_name: str
    platform_name: str
    steps: tuple[PlanStep, ...] = field(default_factory=tuple)

    @property
    def has_blocked_steps(self) -> bool:
        return any(step.action == "blocked" for step in self.steps)

    def to_text(self) -> str:
        lines = [f"profile: {self.profile_name}", f"platform: {self.platform_name}"]
        if not self.steps:
            lines.append("- no changes required")
            return "\n".join(lines)

        for step in self.steps:
            details = f"- [{step.action}] {step.module_name}: {step.reason}"
            if step.dependencies:
                details += f" | depends_on={','.join(step.dependencies)}"
            if step.blocked_by:
                details += f" | blocked_by={','.join(step.blocked_by)}"
            lines.append(details)
        return "\n".join(lines)
