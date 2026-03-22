from __future__ import annotations

import platform


def detect_platform() -> str:
    system_name = platform.system().lower()
    if system_name == "windows":
        return "windows"
    if system_name == "linux":
        return "linux"
    return "unknown"
