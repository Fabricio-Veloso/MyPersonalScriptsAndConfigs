from __future__ import annotations

from personal_setup.adapters.shell import command_exists
from personal_setup.models.module import CheckResult, ModuleDefinition
from personal_setup.modules.base import BaseModule


class NeovimModule(BaseModule):
    definition = ModuleDefinition(
        name="neovim",
        description="Ensure Neovim is available",
        supported_platforms=("windows", "linux"),
        dependencies=("git",),
    )

    def check(self) -> CheckResult:
        ready = command_exists("nvim")
        return CheckResult(
            "neovim",
            True,
            ready,
            install_required=not ready,
            details="nvim available in PATH" if ready else "nvim is not available in PATH",
        )

    def apply(self) -> None:
        return None

    def verify(self) -> CheckResult:
        return self.check()
