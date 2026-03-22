from __future__ import annotations

import shutil
from pathlib import Path


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def path_exists(path: Path) -> bool:
    return path.exists()


def copy_file(source: Path, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def files_match(source: Path, destination: Path) -> bool:
    if not source.exists() or not destination.exists():
        return False

    return source.read_text(encoding="utf-8") == destination.read_text(encoding="utf-8")
