from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from personal_setup.modules.neovim import NeovimModule


class NeovimModuleTest(unittest.TestCase):
    def test_check_requires_install_and_config_when_binary_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source_dir = temp_path / "source"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "init.lua").write_text("return {}\n", encoding="utf-8")

            module = NeovimModule(
                PROJECT_ROOT,
                platform_name="linux",
                config_source_dir=source_dir,
                config_destination_dir=temp_path / "destination",
                command_exists_fn=lambda command: command == "lua",
                apt_available_fn=lambda: True,
            )

            result = module.check()

            self.assertTrue(result.install_required)
            self.assertTrue(result.configure_required)
            self.assertEqual(result.preferred_action, "install")

    def test_check_blocks_when_no_local_or_public_remote_source_is_available(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            module = NeovimModule(
                PROJECT_ROOT,
                platform_name="linux",
                config_source_dir=temp_path / "missing-source",
                config_destination_dir=temp_path / "destination",
                config_repo_url="https://github.com/example/private-config",
                command_exists_fn=lambda _: True,
                apt_available_fn=lambda: True,
                run_fn=lambda command, *, cwd=None, env=None: SimpleNamespace(returncode=1, stdout="", stderr="not found"),
            )

            result = module.check()

            self.assertEqual(result.status_label, "blocked")
            self.assertIn("no usable Neovim config source", result.blocked_reason)

    def test_check_reports_public_remote_repo_when_local_source_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            def fake_run(command: list[str], *, cwd=None, env=None):
                if command[:2] == ["git", "ls-remote"]:
                    return SimpleNamespace(returncode=0, stdout="HEAD\n", stderr="")
                self.fail(f"unexpected command: {command}")

            module = NeovimModule(
                PROJECT_ROOT,
                platform_name="linux",
                config_source_dir=temp_path / "missing-source",
                config_destination_dir=temp_path / "destination",
                config_repo_url="https://github.com/Fabricio-Veloso/NvimConfig",
                command_exists_fn=lambda command: command in {"git", "nvim", "lua"},
                apt_available_fn=lambda: True,
                run_fn=fake_run,
            )

            result = module.check()

            self.assertFalse(result.ready)
            self.assertTrue(result.configure_required)
            self.assertIn("repository is public", result.details)

    def test_check_uses_repo_url_from_getter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            seen_commands: list[list[str]] = []

            def fake_run(command: list[str], *, cwd=None, env=None):
                seen_commands.append(command)
                return SimpleNamespace(returncode=0, stdout="HEAD\n", stderr="")

            module = NeovimModule(
                PROJECT_ROOT,
                platform_name="linux",
                config_source_dir=temp_path / "missing-source",
                config_destination_dir=temp_path / "destination",
                config_repo_url_getter=lambda: "https://github.com/Fabricio-Veloso/NvimConfig",
                command_exists_fn=lambda command: command in {"git", "nvim", "lua"},
                apt_available_fn=lambda: True,
                run_fn=fake_run,
            )

            result = module.check()

            self.assertTrue(result.configure_required)
            self.assertIn(
                ["git", "ls-remote", "https://github.com/Fabricio-Veloso/NvimConfig", "HEAD"],
                seen_commands,
            )

    def test_check_blocks_when_required_runtime_dependency_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = Path(temp_dir) / "nvim"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "init.lua").write_text("return {}\n", encoding="utf-8")

            module = NeovimModule(
                PROJECT_ROOT,
                platform_name="linux",
                config_source_dir=source_dir,
                config_destination_dir=source_dir,
                command_exists_fn=lambda command: command == "nvim",
                apt_available_fn=lambda: True,
            )

            result = module.check()

            self.assertEqual(result.status_label, "blocked")
            self.assertIn("lua", result.blocked_reason)

    def test_apply_installs_neovim_and_copies_local_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source_dir = temp_path / "source"
            destination_dir = temp_path / "destination"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "init.lua").write_text("require('core')\n", encoding="utf-8")
            (source_dir / "lazy-lock.json").write_text("{}\n", encoding="utf-8")

            install_state = {"nvim": False}
            install_calls: list[str] = []

            def fake_command_exists(command: str) -> bool:
                if command == "nvim":
                    return install_state["nvim"]
                return command in {"git", "lua"}

            def fake_apt_install(package_name: str):
                install_calls.append(package_name)
                install_state["nvim"] = True
                return SimpleNamespace(returncode=0, stdout="", stderr="")

            module = NeovimModule(
                PROJECT_ROOT,
                platform_name="linux",
                config_source_dir=source_dir,
                config_destination_dir=destination_dir,
                command_exists_fn=fake_command_exists,
                apt_available_fn=lambda: True,
                apt_install_fn=fake_apt_install,
            )

            module.apply()

            self.assertEqual(install_calls, ["neovim"])
            self.assertTrue((destination_dir / "init.lua").exists())
            self.assertTrue((destination_dir / "lazy-lock.json").exists())

    def test_apply_clones_remote_config_when_local_source_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            destination_dir = temp_path / "destination"

            def fake_run(command: list[str], *, cwd=None, env=None):
                if command[:2] == ["git", "ls-remote"]:
                    return SimpleNamespace(returncode=0, stdout="HEAD\n", stderr="")
                if command[:3] == ["git", "clone", "--depth"]:
                    clone_target = Path(command[-1])
                    clone_target.mkdir(parents=True, exist_ok=True)
                    (clone_target / "init.lua").write_text("print('repo')\n", encoding="utf-8")
                    return SimpleNamespace(returncode=0, stdout="", stderr="")
                self.fail(f"unexpected command: {command}")

            module = NeovimModule(
                PROJECT_ROOT,
                platform_name="linux",
                config_source_dir=temp_path / "missing-source",
                config_destination_dir=destination_dir,
                config_repo_url="https://github.com/Fabricio-Veloso/NvimConfig",
                command_exists_fn=lambda command: command in {"git", "nvim", "lua"},
                apt_available_fn=lambda: True,
                run_fn=fake_run,
            )

            module.apply()

            self.assertTrue((destination_dir / "init.lua").exists())

    def test_verify_runs_in_isolated_directories_and_cleans_them_up(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = Path(temp_dir) / "nvim"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "init.lua").write_text("print('hello')\n", encoding="utf-8")

            captured: dict[str, object] = {}

            def fake_run(command: list[str], *, cwd=None, env=None):
                captured["command"] = command
                captured["cwd"] = cwd
                captured["env"] = env
                isolated_init = Path(env["XDG_CONFIG_HOME"]) / env["NVIM_APPNAME"] / "init.lua"
                captured["isolated_init_exists_during_run"] = isolated_init.exists()
                captured["isolated_root"] = Path(env["XDG_CONFIG_HOME"]).parent
                return SimpleNamespace(returncode=0, stdout="", stderr="")

            module = NeovimModule(
                PROJECT_ROOT,
                platform_name="linux",
                config_source_dir=source_dir,
                config_destination_dir=source_dir,
                command_exists_fn=lambda _: True,
                apt_available_fn=lambda: True,
                run_fn=fake_run,
            )

            result = module.verify()

            self.assertTrue(result.ready)
            self.assertEqual(
                captured["command"],
                ["nvim", "--headless", "+lua pcall(require, 'lazy')", "+checkhealth", "+qa"],
            )
            self.assertTrue(captured["isolated_init_exists_during_run"])
            self.assertFalse(Path(captured["isolated_root"]).exists())
            self.assertIn("smoke verify succeeded", result.details)
            self.assertEqual(result.warnings, ())

    def test_verify_reports_headless_startup_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = Path(temp_dir) / "nvim"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "init.lua").write_text("print('hello')\n", encoding="utf-8")

            module = NeovimModule(
                PROJECT_ROOT,
                platform_name="linux",
                config_source_dir=source_dir,
                config_destination_dir=source_dir,
                command_exists_fn=lambda _: True,
                apt_available_fn=lambda: True,
                run_fn=lambda command, *, cwd=None, env=None: SimpleNamespace(
                    returncode=1,
                    stdout="",
                    stderr="missing dependency",
                ),
            )

            result = module.verify()

            self.assertFalse(result.ready)
            self.assertIn("isolated Neovim smoke verify failed", result.details)
            self.assertIn("missing dependency", result.details)

    def test_apply_clones_remote_config_using_repo_url_getter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            destination_dir = temp_path / "destination"
            seen_commands: list[list[str]] = []

            def fake_run(command: list[str], *, cwd=None, env=None):
                seen_commands.append(command)
                if command[:2] == ["git", "ls-remote"]:
                    return SimpleNamespace(returncode=0, stdout="HEAD\n", stderr="")
                if command[:3] == ["git", "clone", "--depth"]:
                    clone_target = Path(command[-1])
                    clone_target.mkdir(parents=True, exist_ok=True)
                    (clone_target / "init.lua").write_text("print('repo')\n", encoding="utf-8")
                    return SimpleNamespace(returncode=0, stdout="", stderr="")
                self.fail(f"unexpected command: {command}")

            module = NeovimModule(
                PROJECT_ROOT,
                platform_name="linux",
                config_source_dir=temp_path / "missing-source",
                config_destination_dir=destination_dir,
                config_repo_url_getter=lambda: "https://github.com/Fabricio-Veloso/NvimConfig",
                command_exists_fn=lambda command: command in {"git", "nvim", "lua"},
                apt_available_fn=lambda: True,
                run_fn=fake_run,
            )

            module.apply()

            self.assertTrue((destination_dir / "init.lua").exists())
            self.assertIn(
                ["git", "clone", "--depth", "1", "https://github.com/Fabricio-Veloso/NvimConfig", str(destination_dir)],
                seen_commands,
            )


if __name__ == "__main__":
    unittest.main()
