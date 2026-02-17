"""
Task 2: Variables and Data Types
"""

from __future__ import annotations
from typing import Any, Dict

def add_integers(a: int, b: int) -> int:
    return a + b

def divide_floats(a: float, b: float) -> float:
    return a / b

def concat_strings(a: str, b: str) -> str:
    return f"{a}{b}"

def toggle_boolean(value: bool) -> bool:
    return not value

def sample_values() -> Dict[str, Any]:
    return {
        "count": 3,            # int
        "ratio": 0.25,         # float
        "label": "hello",      # str
        "enabled": True,       # bool
    }

def main() -> None:
    values = sample_values()

    print("Sample values:", values)
    print("add_integers(2, 5) =", add_integers(2, 5))
    print("divide_floats(10.0, 4.0) =", divide_floats(10.0, 4.0))
    print('concat_strings("he", "llo") =', concat_strings("he", "llo"))
    print("toggle_boolean(True) =", toggle_boolean(True))

if __name__ == "__main__":
    main()