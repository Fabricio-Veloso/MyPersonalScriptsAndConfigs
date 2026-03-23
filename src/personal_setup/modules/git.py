from __future__ import annotations

from personal_setup.adapters.shell import command_exists
from personal_setup.models.module import CheckResult, ModuleDefinition
from personal_setup.modules.base import BaseModule


class GitModule(BaseModule):
    definition = ModuleDefinition(
        name="git",
        description="Ensure Git is available on the machine",
        supported_platforms=("windows", "linux"),
    )

    def check(self) -> CheckResult:
        ready = command_exists("git")
        return CheckResult(
            "git",
            True,
            ready,
            install_required=not ready,
            details="git available in PATH" if ready else "git is not available in PATH",
        )

    def apply(self) -> None:
        return None

    def verify(self, *, sandbox: bool = False) -> CheckResult:
        return self.check()
