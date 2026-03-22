from __future__ import annotations

from personal_setup.adapters.shell import run


def run_powershell(command: str):
    return run(["pwsh", "-NoProfile", "-Command", command])
