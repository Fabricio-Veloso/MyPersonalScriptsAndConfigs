from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Profile:
    name: str
    modules: tuple[str, ...]
    description: str = ""
    variables: dict[str, str] = field(default_factory=dict)
