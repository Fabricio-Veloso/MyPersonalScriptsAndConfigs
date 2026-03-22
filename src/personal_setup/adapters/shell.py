from __future__ import annotations

import shutil
import subprocess


def command_exists(command_name: str) -> bool:
    return shutil.which(command_name) is not None


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, text=True, capture_output=True)
