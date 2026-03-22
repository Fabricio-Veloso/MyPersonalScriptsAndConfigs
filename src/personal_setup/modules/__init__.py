from __future__ import annotations

from pathlib import Path

from personal_setup.modules.autohotkey import AutoHotkeyModule
from personal_setup.modules.git import GitModule
from personal_setup.modules.glazewm import GlazeWMModule
from personal_setup.modules.neovim import NeovimModule
from personal_setup.modules.project_folders import ProjectFoldersModule


def build_module_registry(project_root: Path, user_settings) -> dict[str, object]:
    modules = [
        GitModule(project_root),
        ProjectFoldersModule(project_root, user_settings),
        NeovimModule(project_root),
        AutoHotkeyModule(project_root),
        GlazeWMModule(project_root),
    ]
    return {module.definition.name: module for module in modules}
