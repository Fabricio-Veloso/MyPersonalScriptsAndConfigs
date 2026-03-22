from __future__ import annotations

from pathlib import Path

from personal_setup.adapters.filesystem import copy_file, ensure_directory, files_match
from personal_setup.adapters.shell import command_exists
from personal_setup.adapters.winget import install as winget_install
from personal_setup.adapters.winget import is_available as winget_is_available
from personal_setup.adapters.winget import is_installed as winget_is_installed
from personal_setup.adapters.windows import create_shortcut, read_shortcut_target, startup_dir
from personal_setup.models.module import CheckResult, ModuleDefinition
from personal_setup.modules.base import BaseModule


class GlazeWMModule(BaseModule):
    definition = ModuleDefinition(
        name="glazewm",
        description="Ensure GlazeWM config is present on Windows",
        supported_platforms=("windows",),
    )

    def __init__(
        self,
        project_root: Path,
        *,
        config_dir: Path | None = None,
        startup_directory: Path | None = None,
        executable_path: Path | None = None,
        command_exists_fn=command_exists,
        winget_available_fn=winget_is_available,
        winget_installed_fn=winget_is_installed,
        winget_install_fn=winget_install,
        copy_file_fn=copy_file,
        files_match_fn=files_match,
        create_shortcut_fn=create_shortcut,
        read_shortcut_target_fn=read_shortcut_target,
    ) -> None:
        super().__init__(project_root)
        self.config_dir = config_dir or (Path.home() / ".glzr" / "glazewm")
        self.startup_directory = startup_directory or startup_dir()
        self.executable_path = executable_path or Path("C:/Program Files/glzr.io/GlazeWM/cli/glazewm.exe")
        self.command_exists_fn = command_exists_fn
        self.winget_available_fn = winget_available_fn
        self.winget_installed_fn = winget_installed_fn
        self.winget_install_fn = winget_install_fn
        self.copy_file_fn = copy_file_fn
        self.files_match_fn = files_match_fn
        self.create_shortcut_fn = create_shortcut_fn
        self.read_shortcut_target_fn = read_shortcut_target_fn

    def _config_source(self) -> Path:
        return self.project_root / "assets" / "glazewm" / "config.yaml"

    def _default_config_path(self) -> Path:
        return self.config_dir / "config.yaml"

    def _startup_shortcut_path(self) -> Path:
        return self.startup_directory / "GlazeWM.lnk"

    def _is_installed(self) -> bool:
        return (
            self.command_exists_fn("glazewm.exe")
            or self.executable_path.exists()
            or self.winget_installed_fn("glzr-io.glazewm")
        )

    def _startup_matches(self) -> bool:
        shortcut_path = self._startup_shortcut_path()
        if not shortcut_path.exists():
            return False

        return Path(self.read_shortcut_target_fn(shortcut_path)) == self.executable_path

    def check(self) -> CheckResult:
        if not self.is_supported_on_current_platform():
            return CheckResult("glazewm", False, False, details="GlazeWM only applies to Windows")

        installed = self._is_installed()
        config_ready = self.files_match_fn(self._config_source(), self._default_config_path())
        startup_ready = self._startup_matches()
        ready = installed and config_ready and startup_ready

        details_parts: list[str] = []
        if not installed:
            details_parts.append("GlazeWM executable not found")
        if not config_ready:
            details_parts.append(f"GlazeWM config missing or different at {self._default_config_path()}")
        if not startup_ready:
            details_parts.append(f"GlazeWM startup shortcut missing or different at {self._startup_shortcut_path()}")
        if ready:
            details_parts.append("GlazeWM executable, config and startup shortcut are available")

        blocked_reason = ""
        if not installed and not self.winget_available_fn():
            blocked_reason = "winget is required to install GlazeWM automatically on Windows"

        return CheckResult(
            "glazewm",
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
            result = self.winget_install_fn("glzr-io.glazewm")
            installed_after = self._is_installed()
            if getattr(result, "returncode", 0) != 0 and not installed_after:
                raise RuntimeError("failed to install GlazeWM with winget")

        destination = self._default_config_path()
        ensure_directory(destination.parent)
        self.copy_file_fn(self._config_source(), destination)

        shortcut_result = self.create_shortcut_fn(self._startup_shortcut_path(), self.executable_path)
        if getattr(shortcut_result, "returncode", 0) != 0 and not self._startup_matches():
            raise RuntimeError("failed to create GlazeWM startup shortcut")

    def verify(self) -> CheckResult:
        return self.check()
