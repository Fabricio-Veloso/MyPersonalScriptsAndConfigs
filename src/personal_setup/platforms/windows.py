from __future__ import annotations

from pathlib import Path


def default_config_home() -> Path:
    return Path.home() / "AppData" / "Local"
