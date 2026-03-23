from __future__ import annotations

import argparse
from collections.abc import Callable

from personal_setup.app import create_app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="personal-setup")
    subparsers = parser.add_subparsers(dest="command", required=False)

    for command_name in ("plan", "apply", "check", "verify"):
        command_parser = subparsers.add_parser(command_name)
        command_parser.add_argument("--profile", default="full")
        if command_name == "verify":
            command_parser.add_argument("--sandbox", action="store_true")

    configure_user_parser = subparsers.add_parser("configure-user")
    configure_user_parser.add_argument("--name")

    configure_neovim_parser = subparsers.add_parser("configure-neovim")
    configure_neovim_parser.add_argument("--repo-url")

    return parser


def prompt_user_name() -> str:
    while True:
        user_name = input("Digite o nome que devo usar para sua pasta principal: ").strip()
        if user_name:
            return user_name

        print("Nome invalido. Tente novamente.")


def print_menu() -> None:
    print("Personal Setup CLI")
    print("1. Configure user")
    print("2. Plan")
    print("3. Apply")
    print("4. Check")
    print("5. Verify")
    print("6. Configure Neovim repo")
    print("0. Exit")


def run_interactive_menu(app, input_func: Callable[[str], str] | None = None) -> int:
    if input_func is None:
        input_func = input

    while True:
        print_menu()
        choice = input_func("Escolha uma opcao: ").strip()

        if choice == "0":
            print("Saindo.")
            return 0

        if choice == "1":
            user_name = input_func("Digite o nome que devo usar para sua pasta principal: ").strip()
            if not user_name:
                print("Nome invalido. Tente novamente.")
                continue
            saved_path = app.configure_user_name(user_name)
            print(f"user name saved: {user_name}")
            print(f"settings file: {saved_path}")
            continue

        if choice == "2":
            try:
                print(app.plan("full").to_text())
            except Exception as exc:
                print(f"Erro ao executar plan: {exc}")
            continue

        if choice == "3":
            try:
                print(app.apply("full").to_text())
            except Exception as exc:
                print(f"Erro ao executar apply: {exc}")
            continue

        if choice == "4":
            try:
                print(app.check("full").to_text())
            except Exception as exc:
                print(f"Erro ao executar check: {exc}")
            continue

        if choice == "5":
            try:
                print(app.verify("full").to_text())
            except Exception as exc:
                print(f"Erro ao executar verify: {exc}")
            continue

        if choice == "6":
            repo_url = input_func("Digite a URL do repo da configuracao do Neovim: ").strip()
            if not repo_url:
                print("URL invalida. Tente novamente.")
                continue
            saved_path = app.configure_neovim_repo_url(repo_url)
            print(f"neovim repo saved: {repo_url}")
            print(f"settings file: {saved_path}")
            continue

        print("Opcao invalida. Tente novamente.")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    app = create_app()

    if args.command is None:
        return run_interactive_menu(app)

    if args.command == "plan":
        result = app.plan(args.profile)
        print(result.to_text())
        return 0

    if args.command == "apply":
        result = app.apply(args.profile)
        print(result.to_text())
        return 0

    if args.command == "check":
        result = app.check(args.profile)
        print(result.to_text())
        return 0

    if args.command == "verify":
        result = app.verify(args.profile, sandbox=args.sandbox)
        print(result.to_text())
        return 0

    if args.command == "configure-user":
        user_name = args.name or prompt_user_name()
        saved_path = app.configure_user_name(user_name)
        print(f"user name saved: {user_name}")
        print(f"settings file: {saved_path}")
        return 0

    if args.command == "configure-neovim":
        repo_url = args.repo_url
        if not repo_url:
            parser.error("configure-neovim requires --repo-url")
        saved_path = app.configure_neovim_repo_url(repo_url)
        print(f"neovim repo saved: {repo_url}")
        print(f"settings file: {saved_path}")
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
