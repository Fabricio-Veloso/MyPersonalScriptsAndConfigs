from __future__ import annotations

from pathlib import Path
import tomllib

from personal_setup.models.profile import Profile


class ProfileLoader:
    def __init__(self, profiles_dir: Path) -> None:
        self.profiles_dir = profiles_dir

    def load(self, profile_name: str) -> Profile:
        profile_path = self.profiles_dir / f"{profile_name}.toml"
        data = tomllib.loads(profile_path.read_text(encoding="utf-8"))
        return Profile(
            name=data["name"],
            description=data.get("description", ""),
            modules=tuple(data.get("modules", [])),
            variables=dict(data.get("variables", {})),
        )
