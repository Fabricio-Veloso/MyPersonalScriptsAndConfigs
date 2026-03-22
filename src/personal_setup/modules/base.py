from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from personal_setup.models.module import CheckResult, ModuleDefinition
from personal_setup.platforms.base import detect_platform


class BaseModule(ABC):
    definition: ModuleDefinition

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def is_supported_on_current_platform(self) -> bool:
        return detect_platform() in self.definition.supported_platforms

    @abstractmethod
    def check(self) -> CheckResult:
        raise NotImplementedError

    @abstractmethod
    def apply(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def verify(self) -> CheckResult:
        raise NotImplementedError
