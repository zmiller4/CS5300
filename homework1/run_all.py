from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> int:
    print(f"\n$ {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=str(cwd))


def main() -> int:
    hw = Path(__file__).resolve().parent
    src = hw / "src"

    if not src.exists():
        print(f"Missing src directory: {src}")
        return 1

    # Run every task*.py in src/
    # Sort them by file name so they run in order
    task_files = sorted(src.glob("task*.py"), key=lambda p: p.name)
    if not task_files:
        print(f"No task*.py files found in: {src}")
        return 1

    for task in task_files:
        code = run([sys.executable, str(task)], cwd=hw)
        if code != 0:
            print(f"{task.name} failed with exit code {code}")
            return code

    # Run pytest
    code = run([sys.executable, "-m", "pytest", "-q"], cwd=hw)
    if code != 0:
        print(f"pytest failed with exit code {code}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
