from __future__ import annotations

from pathlib import Path

from personal_setup.models.module import CheckResult, ModuleDefinition
from personal_setup.modules.base import BaseModule
from personal_setup.platforms.base import detect_platform


class ProjectFoldersModule(BaseModule):
    definition = ModuleDefinition(
        name="project_folders",
        description="Ensure the default projects folder exists",
        supported_platforms=("windows", "linux"),
    )

    def __init__(
        self,
        project_root: Path,
        user_settings,
        *,
        platform_name: str | None = None,
        windows_root: Path | None = None,
        linux_home: Path | None = None,
    ) -> None:
        super().__init__(project_root)
        self.user_settings = user_settings
        self.platform_name = platform_name
        self.windows_root = windows_root or Path("C:/")
        self.linux_home = linux_home or Path.home()

    def _current_platform(self) -> str:
        return self.platform_name or detect_platform()

    def _projects_dir(self) -> Path | None:
        platform_name = self._current_platform()
        if platform_name == "windows":
            user_name = self.user_settings.load_user_name()
            if not user_name:
                return None
            return self.windows_root / user_name / "projects"

        return self.linux_home / "projects"

    def check(self) -> CheckResult:
        path = self._projects_dir()
        if path is None:
            return CheckResult(
                "project_folders",
                True,
                False,
                configure_required=True,
                details="configure-user must be run before planning project folders on Windows",
                blocked_reason="missing configured user name for Windows project folder",
            )

        ready = path.exists() and path.is_dir()
        return CheckResult(
            "project_folders",
            True,
            ready,
            configure_required=not ready,
            details=f"projects directory: {path}",
        )

    def apply(self) -> None:
        path = self._projects_dir()
        if path is None:
            raise RuntimeError("User name must be configured before applying project_folders on Windows")
        path.mkdir(parents=True, exist_ok=True)

    def verify(self, *, sandbox: bool = False) -> CheckResult:
        return self.check()
