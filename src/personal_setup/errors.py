from __future__ import annotations


class SetupError(Exception):
    """Base error for setup application failures."""


class PlanningError(SetupError):
    """Base error for planning failures."""


class UnknownModuleError(PlanningError):
    def __init__(self, module_name: str) -> None:
        super().__init__(f"Unknown module referenced by profile: {module_name}")
        self.module_name = module_name


class MissingDependencyError(PlanningError):
    def __init__(self, module_name: str, dependency_name: str) -> None:
        super().__init__(
            f"Module '{module_name}' depends on missing module '{dependency_name}'"
        )
        self.module_name = module_name
        self.dependency_name = dependency_name


class CircularDependencyError(PlanningError):
    def __init__(self, dependency_chain: tuple[str, ...]) -> None:
        chain_text = " -> ".join(dependency_chain)
        super().__init__(f"Circular dependency detected: {chain_text}")
        self.dependency_chain = dependency_chain
