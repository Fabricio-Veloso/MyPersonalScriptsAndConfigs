from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ModuleDefinition:
    name: str
    description: str
    supported_platforms: tuple[str, ...]
    dependencies: tuple[str, ...] = ()


@dataclass(frozen=True)
class ModuleStatus:
    value: str
    reason: str = ""


@dataclass(frozen=True)
class CheckResult:
    module_name: str
    applicable: bool
    ready: bool
    install_required: bool = False
    configure_required: bool = False
    details: str = ""
    warnings: tuple[str, ...] = field(default_factory=tuple)
    blocked_reason: str = ""

    @property
    def status_label(self) -> str:
        if self.blocked_reason:
            return "blocked"
        if not self.applicable:
            return "not-applicable"
        if self.ready:
            return "ready"
        if self.install_required and self.configure_required:
            return "missing-install-and-config"
        if self.install_required:
            return "missing-install"
        if self.configure_required:
            return "missing-config"
        return "missing"

    @property
    def requires_action(self) -> bool:
        return self.applicable and not self.ready and not self.blocked_reason

    @property
    def preferred_action(self) -> str:
        if self.blocked_reason:
            return "blocked"
        if not self.applicable:
            return "skip"
        if self.ready:
            return "keep"
        if self.install_required:
            return "install"
        if self.configure_required:
            return "configure"
        return "apply"
