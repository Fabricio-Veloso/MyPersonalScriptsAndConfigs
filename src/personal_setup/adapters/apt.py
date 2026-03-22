from __future__ import annotations

from personal_setup.adapters.shell import command_exists, run


def is_available() -> bool:
    return command_exists("apt")


def install(package_name: str):
    return run(["sudo", "apt", "install", "-y", package_name])
