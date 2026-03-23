from __future__ import annotations

import json
from pathlib import Path


class UserSettingsStore:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def _load_data(self) -> dict[str, object]:
        if not self.file_path.exists():
            return {}

        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _load_string(self, key: str) -> str | None:
        data = self._load_data()
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            return None
        return value.strip()

    def _save_string(self, key: str, value: str) -> Path:
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{key} cannot be empty")

        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = self._load_data()
        payload[key] = normalized
        self.file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return self.file_path

    def load_user_name(self) -> str | None:
        return self._load_string("user_name")

    def save_user_name(self, user_name: str) -> Path:
        return self._save_string("user_name", user_name)

    def load_neovim_repo_url(self) -> str | None:
        return self._load_string("neovim_repo_url")

    def save_neovim_repo_url(self, repo_url: str) -> Path:
        return self._save_string("neovim_repo_url", repo_url)
