from __future__ import annotations

from pathlib import Path

from personal_setup.adapters.shell import run


def startup_dir() -> Path:
    return Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"


def create_shortcut(shortcut_path: Path, target_path: Path, arguments: str = ""):
    shortcut_path.parent.mkdir(parents=True, exist_ok=True)
    command = (
        "$shell = New-Object -ComObject WScript.Shell; "
        f"$shortcut = $shell.CreateShortcut('{str(shortcut_path)}'); "
        f"$shortcut.TargetPath = '{str(target_path)}'; "
        f"$shortcut.Arguments = '{arguments}'; "
        "$shortcut.Save()"
    )
    return run(["powershell", "-NoProfile", "-Command", command])


def read_shortcut_target(shortcut_path: Path) -> str:
    command = (
        f"(New-Object -ComObject WScript.Shell).CreateShortcut('{str(shortcut_path)}').TargetPath"
    )
    result = run(["powershell", "-NoProfile", "-Command", command])
    return result.stdout.strip()
