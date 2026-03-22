from __future__ import annotations

from pathlib import Path

from personal_setup.adapters.filesystem import copy_file, ensure_directory, files_match
from personal_setup.adapters.shell import command_exists
from personal_setup.adapters.winget import install as winget_install
from personal_setup.adapters.winget import is_available as winget_is_available
from personal_setup.adapters.winget import is_installed as winget_is_installed
from personal_setup.adapters.windows import startup_dir
from personal_setup.models.module import CheckResult, ModuleDefinition
from personal_setup.modules.base import BaseModule


class AutoHotkeyModule(BaseModule):
    definition = ModuleDefinition(
        name="autohotkey",
        description="Ensure AutoHotkey is available and config can be managed",
        supported_platforms=("windows",),
    )

    def __init__(
        self,
        project_root: Path,
        *,
        documents_dir: Path | None = None,
        startup_directory: Path | None = None,
        command_exists_fn=command_exists,
        winget_available_fn=winget_is_available,
        winget_installed_fn=winget_is_installed,
        winget_install_fn=winget_install,
        copy_file_fn=copy_file,
        files_match_fn=files_match,
    ) -> None:
        super().__init__(project_root)
        self.documents_dir = documents_dir or (Path.home() / "Documents")
        self.startup_directory = startup_directory or startup_dir()
        self.command_exists_fn = command_exists_fn
        self.winget_available_fn = winget_available_fn
        self.winget_installed_fn = winget_installed_fn
        self.winget_install_fn = winget_install_fn
        self.copy_file_fn = copy_file_fn
        self.files_match_fn = files_match_fn

    def _config_source(self) -> Path:
        return self.project_root / "assets" / "autohotkey" / "main.ahk"

    def _config_destination(self) -> Path:
        return self.documents_dir / "AutoHotkey" / "main.ahk"

    def _startup_script_destination(self) -> Path:
        return self.startup_directory / "mainScript.ahk"

    def _is_installed(self) -> bool:
        return (
            self.command_exists_fn("AutoHotkey64.exe")
            or self.command_exists_fn("AutoHotkey.exe")
            or self.winget_installed_fn("AutoHotkey.AutoHotkey")
        )

    def check(self) -> CheckResult:
        if not self.is_supported_on_current_platform():
            return CheckResult("autohotkey", False, False, details="AutoHotkey only applies to Windows")

        installed = self._is_installed()
        config_ready = self.files_match_fn(self._config_source(), self._config_destination())
        startup_ready = self.files_match_fn(self._config_source(), self._startup_script_destination())
        ready = installed and config_ready and startup_ready

        details_parts: list[str] = []
        if not installed:
            details_parts.append("AutoHotkey executable not found")
        if not config_ready:
            details_parts.append(f"AutoHotkey config missing at {self._config_destination()}")
        if not startup_ready:
            details_parts.append(f"AutoHotkey startup script missing at {self._startup_script_destination()}")
        if ready:
            details_parts.append("AutoHotkey executable, config and startup script are available")

        blocked_reason = ""
        if not installed and not self.winget_available_fn():
            blocked_reason = "winget is required to install AutoHotkey automatically on Windows"

        return CheckResult(
            "autohotkey",
            True,
            ready,
            install_required=not installed,
            configure_required=not config_ready or not startup_ready,
            details="; ".join(details_parts),
            blocked_reason=blocked_reason,
        )

    def apply(self) -> None:
        check_result = self.check()
        if check_result.blocked_reason:
            raise RuntimeError(check_result.blocked_reason)

        if check_result.install_required:
            result = self.winget_install_fn("AutoHotkey.AutoHotkey")
            if getattr(result, "returncode", 0) != 0 and not self._is_installed():
                command_output = "\n".join(
                    part.strip()
                    for part in (
                        getattr(result, "stdout", ""),
                        getattr(result, "stderr", ""),
                    )
                    if part and part.strip()
                )
                message = "failed to install AutoHotkey with winget"
                if command_output:
                    message = f"{message}: {command_output}"
                raise RuntimeError(message)

        destination = self._config_destination()
        ensure_directory(destination.parent)
        self.copy_file_fn(self._config_source(), destination)
        self.copy_file_fn(self._config_source(), self._startup_script_destination())

    def verify(self) -> CheckResult:
        return self.check()
