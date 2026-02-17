"""
Task 5: Lists and Dictionaries
"""

from __future__ import annotations
from typing import Dict, List, Tuple

def favorite_books() -> List[Tuple[str, str]]:
    return [
        ("The Way of Shadows", "Brent Weeks"),
        ("Cat's Cradle", "Kurt Vonnegut, Jr."),
        ("Harry Potter", "J.K. Rowling"),
        ("The Scholomance Series", "Naomi Novik"),
    ]

def first_three_books(books: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    return books[:3]

def student_db() -> Dict[str, int]:
    return {
        "Joe Schmoe": 1,
        "John Doe": 2,
        "Jane Doe": 3,
    }

def get_student_id(db: Dict[str, int], name: str) -> int | None:
    return db.get(name)
