from __future__ import annotations

from personal_setup.adapters.shell import command_exists, run


def is_available() -> bool:
    return command_exists("winget")


def is_installed(package_id: str) -> bool:
    result = run(["winget", "list", "--id", package_id, "--exact"])
    if result.returncode != 0:
        return False

    output = "\n".join(part for part in (result.stdout, result.stderr) if part)
    return package_id.lower() in output.lower()


def install(package_id: str):
    return run(
        [
            "winget",
            "install",
            "--id",
            package_id,
            "--exact",
            "--accept-source-agreements",
            "--accept-package-agreements",
        ]
    )
