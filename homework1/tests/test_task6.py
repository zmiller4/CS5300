from __future__ import annotations

from pathlib import Path

import pytest

from task6 import count_words_in_file, count_words_in_text


def test_task6_read_me_word_count_is_104():
    base = Path(__file__).resolve().parents[1]
    file_path = base / "task6_read_me.txt"
    assert count_words_in_file(file_path) == 104


def test_word_count_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        count_words_in_file(tmp_path / "nope.txt")


def test_word_count_directory(tmp_path: Path):
    with pytest.raises(IsADirectoryError):
        count_words_in_file(tmp_path)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("this .", 1),
        ("this.", 1),
        ("well-known author", 2),
        ("don't stop", 2),
        ("  spaced   words \n here\t!", 3),
        ("... !!!", 0),
        ("42 is the answer.", 4),
    ],
)
def test_count_words_in_text_tokenization(text, expected):
    assert count_words_in_text(text) == expected
