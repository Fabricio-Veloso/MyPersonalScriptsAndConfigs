from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def command_exists(command_name: str) -> bool:
    return shutil.which(command_name) is not None


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    completed_env = None
    if env is not None:
        completed_env = os.environ.copy()
        completed_env.update(env)

    return subprocess.run(
        command,
        check=False,
        text=True,
        capture_output=True,
        cwd=cwd,
        env=completed_env,
    )
