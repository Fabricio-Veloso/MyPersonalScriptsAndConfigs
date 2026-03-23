from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

from personal_setup.adapters.apt import install as apt_install
from personal_setup.adapters.apt import is_available as apt_is_available
from personal_setup.adapters.shell import command_exists, run
from personal_setup.adapters.winget import install as winget_install
from personal_setup.adapters.winget import is_available as winget_is_available
from personal_setup.models.module import CheckResult, ModuleDefinition
from personal_setup.modules.base import BaseModule
from personal_setup.platforms.base import detect_platform


class NeovimModule(BaseModule):
    DEFAULT_CONFIG_REPO_URL = "https://github.com/Fabricio-Veloso/NvimConfig"

    definition = ModuleDefinition(
        name="neovim",
        description="Ensure Neovim is available and its config can be validated",
        supported_platforms=("windows", "linux"),
        dependencies=("git",),
    )

    def __init__(
        self,
        project_root: Path,
        *,
        platform_name: str | None = None,
        config_source_dir: Path | None = None,
        config_destination_dir: Path | None = None,
        config_repo_url: str | None = None,
        config_repo_url_getter=None,
        command_exists_fn=command_exists,
        apt_available_fn=apt_is_available,
        apt_install_fn=apt_install,
        winget_available_fn=winget_is_available,
        winget_install_fn=winget_install,
        run_fn=run,
    ) -> None:
        super().__init__(project_root)
        self.platform_name = platform_name
        self.config_source_dir = config_source_dir
        self.config_destination_dir = config_destination_dir
        self.config_repo_url = config_repo_url
        self.config_repo_url_getter = config_repo_url_getter
        self.command_exists_fn = command_exists_fn
        self.apt_available_fn = apt_available_fn
        self.apt_install_fn = apt_install_fn
        self.winget_available_fn = winget_available_fn
        self.winget_install_fn = winget_install_fn
        self.run_fn = run_fn

    def _current_platform(self) -> str:
        return self.platform_name or detect_platform()

    def _default_config_dir(self) -> Path:
        platform_name = self._current_platform()
        if platform_name == "windows":
            local_app_data = os.environ.get("LOCALAPPDATA")
            if local_app_data:
                return Path(local_app_data) / "nvim"
            return Path.home() / "AppData" / "Local" / "nvim"

        return Path.home() / ".config" / "nvim"

    def _local_source_dir(self) -> Path:
        return self.config_source_dir or self._default_config_dir()

    def _destination_dir(self) -> Path:
        return self.config_destination_dir or self._default_config_dir()

    def _current_config_repo_url(self) -> str:
        if self.config_repo_url:
            return self.config_repo_url

        if self.config_repo_url_getter is not None:
            repo_url = self.config_repo_url_getter()
            if repo_url:
                return repo_url

        return os.environ.get("PERSONAL_SETUP_NEOVIM_CONFIG_REPO", self.DEFAULT_CONFIG_REPO_URL)

    def _required_runtime_commands(self) -> tuple[str, ...]:
        return ("lua",)

    def _optional_runtime_commands(self) -> tuple[str, ...]:
        platform_name = self._current_platform()
        if platform_name == "windows":
            return ("rg", "node", "python", "make", "win32yank.exe")
        return ("rg", "node", "python3", "make")

    def _missing_commands(self, command_names: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(command_name for command_name in command_names if not self.command_exists_fn(command_name))

    def _command_output(self, result) -> str:
        output = "\n".join(
            part.strip()
            for part in (getattr(result, "stdout", ""), getattr(result, "stderr", ""))
            if part and part.strip()
        )
        return output.replace("\x00", "")

    def _local_source_is_ready(self) -> bool:
        source_dir = self._local_source_dir()
        return source_dir.exists() and (source_dir / "init.lua").exists()

    def _remote_source_is_configured(self) -> bool:
        return bool(self._current_config_repo_url())

    def _remote_source_is_public(self) -> bool:
        if not self._remote_source_is_configured() or not self.command_exists_fn("git"):
            return False

        result = self.run_fn(["git", "ls-remote", self._current_config_repo_url(), "HEAD"])
        return getattr(result, "returncode", 1) == 0

    def _resolved_source_kind(self) -> str | None:
        if self._local_source_is_ready():
            return "local"
        if self._remote_source_is_configured() and self._remote_source_is_public():
            return "remote"
        return None

    def _iter_managed_files(self, root: Path) -> dict[str, Path]:
        managed_files: dict[str, Path] = {}
        for path in root.rglob("*"):
            if path.is_dir():
                continue

            relative_path = path.relative_to(root)
            if any(part in {".git", "__pycache__"} for part in relative_path.parts):
                continue

            managed_files[relative_path.as_posix()] = path
        return managed_files

    def _destination_has_config(self) -> bool:
        destination_dir = self._destination_dir()
        return destination_dir.exists() and (destination_dir / "init.lua").exists()

    def _config_matches_local_source(self) -> bool:
        source_dir = self._local_source_dir()
        destination_dir = self._destination_dir()
        if not self._local_source_is_ready() or not destination_dir.exists():
            return False

        if source_dir.resolve() == destination_dir.resolve():
            return True

        source_files = self._iter_managed_files(source_dir)
        destination_files = self._iter_managed_files(destination_dir)
        if set(source_files) != set(destination_files):
            return False

        for relative_path, source_file in source_files.items():
            destination_file = destination_files[relative_path]
            if source_file.read_bytes() != destination_file.read_bytes():
                return False

        return True

    def _config_is_ready(self) -> bool:
        source_kind = self._resolved_source_kind()
        if source_kind == "local":
            return self._config_matches_local_source()
        if source_kind == "remote":
            return self._destination_has_config()
        return False

    def _can_install_main_binary(self) -> bool:
        platform_name = self._current_platform()
        if platform_name == "windows":
            return self.winget_available_fn()
        if platform_name == "linux":
            return self.apt_available_fn()
        return False

    def _copy_local_config(self, source_dir: Path, destination_dir: Path) -> None:
        if source_dir.resolve() == destination_dir.resolve():
            return

        if destination_dir.exists():
            shutil.rmtree(destination_dir)

        shutil.copytree(
            source_dir,
            destination_dir,
            ignore=shutil.ignore_patterns(".git", "__pycache__"),
        )

    def _clone_remote_config(self, destination_dir: Path):
        if destination_dir.exists():
            shutil.rmtree(destination_dir)

        return self.run_fn(
            ["git", "clone", "--depth", "1", self._current_config_repo_url(), str(destination_dir)]
        )

    def _materialize_config(self, destination_dir: Path) -> None:
        source_kind = self._resolved_source_kind()
        if source_kind == "local":
            self._copy_local_config(self._local_source_dir(), destination_dir)
            return

        if source_kind == "remote":
            result = self._clone_remote_config(destination_dir)
            if getattr(result, "returncode", 0) != 0 or not (destination_dir / "init.lua").exists():
                command_output = self._command_output(result)
                message = f"failed to clone Neovim config from {self._current_config_repo_url()}"
                if command_output:
                    message = f"{message}: {command_output}"
                raise RuntimeError(message)
            return

        raise RuntimeError("no valid Neovim config source is available")

    def _install_main_binary(self):
        platform_name = self._current_platform()
        if platform_name == "windows":
            return self.winget_install_fn("Neovim.Neovim")
        if platform_name == "linux":
            return self.apt_install_fn("neovim")
        raise RuntimeError(f"unsupported platform for neovim install: {platform_name}")

    def _build_isolated_environment(self, temp_root: Path, app_name: str) -> dict[str, str]:
        env = os.environ.copy()
        env.update(
            {
                "NVIM_APPNAME": app_name,
                "XDG_CONFIG_HOME": str(temp_root / "config"),
                "XDG_DATA_HOME": str(temp_root / "data"),
                "XDG_STATE_HOME": str(temp_root / "state"),
                "XDG_CACHE_HOME": str(temp_root / "cache"),
                "HOME": str(temp_root / "home"),
                "LOCALAPPDATA": str(temp_root / "localappdata"),
                "APPDATA": str(temp_root / "appdata"),
            }
        )
        return env

    def _verify_command(self) -> list[str]:
        return [
            "nvim",
            "--headless",
            "+lua pcall(require, 'lazy')",
            "+checkhealth",
            "+qa",
        ]

    def check(self) -> CheckResult:
        if not self.is_supported_on_current_platform():
            return CheckResult("neovim", False, False, details="Neovim only applies to Windows and Linux")

        destination_dir = self._destination_dir()
        repo_url = self._current_config_repo_url()
        installed = self.command_exists_fn("nvim")
        local_source_ready = self._local_source_is_ready()
        remote_source_configured = self._remote_source_is_configured()
        remote_source_public = self._remote_source_is_public() if not local_source_ready else False
        source_kind = "local" if local_source_ready else "remote" if remote_source_public else None
        config_ready = self._config_is_ready()
        missing_required_commands = self._missing_commands(self._required_runtime_commands())
        missing_optional_commands = self._missing_commands(self._optional_runtime_commands())
        ready = installed and config_ready and not missing_required_commands

        details_parts: list[str] = []
        if not installed:
            details_parts.append("nvim is not available in PATH")
        if source_kind == "local" and not config_ready:
            details_parts.append(f"Neovim config missing or different at {destination_dir}")
        if source_kind == "remote":
            details_parts.append(f"Neovim config repository is public: {repo_url}")
            if not config_ready:
                details_parts.append(f"Neovim config missing at {destination_dir}")
        if source_kind is None:
            if not local_source_ready:
                details_parts.append(f"Neovim local config source missing at {self._local_source_dir()}")
            if remote_source_configured:
                details_parts.append(f"Neovim config repository is not reachable as a public repo: {repo_url}")
        if missing_required_commands:
            details_parts.append(
                "missing required runtime commands: " + ", ".join(missing_required_commands)
            )

        warnings: list[str] = []
        if missing_optional_commands:
            warnings.append("missing optional runtime commands: " + ", ".join(missing_optional_commands))
        blocked_reason = ""
        if source_kind is None:
            blocked_reason = "no usable Neovim config source is available"
        elif missing_required_commands:
            blocked_reason = "missing required Neovim runtime dependencies: " + ", ".join(missing_required_commands)
        elif not installed and not self._can_install_main_binary():
            platform_name = self._current_platform()
            if platform_name == "windows":
                blocked_reason = "winget is required to install Neovim automatically on Windows"
            elif platform_name == "linux":
                blocked_reason = "apt is required to install Neovim automatically on Linux"

        if ready:
            details_parts.append(f"nvim available and config ready at {destination_dir}")
        details_parts.extend(warnings)

        return CheckResult(
            "neovim",
            True,
            ready,
            install_required=not installed,
            configure_required=source_kind is not None and not config_ready,
            details="; ".join(details_parts),
            warnings=tuple(warnings),
            blocked_reason=blocked_reason,
        )

    def apply(self) -> None:
        check_result = self.check()
        if check_result.blocked_reason:
            raise RuntimeError(check_result.blocked_reason)

        if check_result.install_required:
            result = self._install_main_binary()
            if getattr(result, "returncode", 0) != 0 and not self.command_exists_fn("nvim"):
                command_output = "\n".join(
                    part.strip()
                    for part in (getattr(result, "stdout", ""), getattr(result, "stderr", ""))
                    if part and part.strip()
                )
                message = "failed to install Neovim automatically"
                if command_output:
                    message = f"{message}: {command_output}"
                raise RuntimeError(message)

        self._materialize_config(self._destination_dir())

    def verify(self, *, sandbox: bool = False) -> CheckResult:
        check_result = self.check()
        if not check_result.applicable:
            return check_result

        if check_result.blocked_reason or check_result.install_required:
            return check_result

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            app_name = "personal-setup-verify"
            isolated_config_dir = temp_root / "config" / app_name
            isolated_config_dir.parent.mkdir(parents=True, exist_ok=True)
            self._materialize_config(isolated_config_dir)

            env = self._build_isolated_environment(temp_root, app_name)
            result = self.run_fn(
                self._verify_command(),
                cwd=temp_root,
                env=env,
            )

        if getattr(result, "returncode", 0) != 0:
            output = self._command_output(result)
            details = "isolated Neovim smoke verify failed"
            if output:
                details = f"{details}: {output}"
            if check_result.warnings:
                details = f"{details}; " + "; ".join(check_result.warnings)
            return CheckResult(
                "neovim",
                True,
                False,
                details=details,
                warnings=check_result.warnings,
            )

        details = "isolated Neovim smoke verify succeeded"
        if check_result.warnings:
            details = f"{details}; " + "; ".join(check_result.warnings)
        return CheckResult(
            "neovim",
            True,
            True,
            details=details,
            warnings=check_result.warnings,
        )
