from __future__ import annotations

from pathlib import Path

from personal_setup.modules import build_module_registry
from personal_setup.services.checker import Checker
from personal_setup.services.executor import Executor
from personal_setup.services.planner import Planner
from personal_setup.services.profile_loader import ProfileLoader
from personal_setup.services.user_settings import UserSettingsStore
from personal_setup.services.verifier import Verifier


class SetupApplication:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.profile_loader = ProfileLoader(project_root / "profiles")
        self.user_settings = UserSettingsStore(project_root / ".local" / "user_settings.json")
        self.module_registry = build_module_registry(project_root, self.user_settings)
        self.planner = Planner(self.profile_loader, self.module_registry)
        self.executor = Executor(self.planner, self.module_registry)
        self.checker = Checker(self.profile_loader, self.module_registry)
        self.verifier = Verifier(self.profile_loader, self.module_registry)

    def configure_user_name(self, user_name: str) -> Path:
        return self.user_settings.save_user_name(user_name)

    def configure_neovim_repo_url(self, repo_url: str) -> Path:
        return self.user_settings.save_neovim_repo_url(repo_url)

    def get_user_name(self) -> str | None:
        return self.user_settings.load_user_name()

    def get_neovim_repo_url(self) -> str | None:
        return self.user_settings.load_neovim_repo_url()

    def plan(self, profile_name: str):
        return self.planner.build_plan(profile_name)

    def apply(self, profile_name: str):
        return self.executor.apply(profile_name)

    def check(self, profile_name: str):
        return self.checker.check(profile_name)

    def verify(self, profile_name: str, *, sandbox: bool = False):
        return self.verifier.verify(profile_name, sandbox=sandbox)


def create_app() -> SetupApplication:
    project_root = Path(__file__).resolve().parents[2]
    return SetupApplication(project_root)
