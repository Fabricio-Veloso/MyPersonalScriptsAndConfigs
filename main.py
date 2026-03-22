from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root / "src"))

    from personal_setup.cli import main as cli_main

    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
