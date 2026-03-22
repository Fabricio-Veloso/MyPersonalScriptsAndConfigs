from __future__ import annotations

import json
from pathlib import Path


class UserSettingsStore:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load_user_name(self) -> str | None:
        if not self.file_path.exists():
            return None

        data = json.loads(self.file_path.read_text(encoding="utf-8"))
        user_name = data.get("user_name")
        if not isinstance(user_name, str) or not user_name.strip():
            return None
        return user_name.strip()

    def save_user_name(self, user_name: str) -> Path:
        normalized = user_name.strip()
        if not normalized:
            raise ValueError("user_name cannot be empty")

        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"user_name": normalized}
        self.file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return self.file_path
