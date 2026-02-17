"""
Task 6: File Handling
"""

from __future__ import annotations

import re
from pathlib import Path

WORD_REGEX = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*")


def count_words_in_text(text: str) -> int:
    return len(WORD_REGEX.findall(text))


def count_words_in_file(path: str | Path, encoding: str = "utf-8") -> int:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))
    if p.is_dir():
        raise IsADirectoryError(str(p))
    return count_words_in_text(p.read_text(encoding=encoding))
