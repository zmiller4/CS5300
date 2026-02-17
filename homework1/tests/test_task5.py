from task5 import favorite_books, first_three_books, get_student_id, student_db


def test_favorite_books_structure():
    books = favorite_books()
    assert len(books) >= 3
    for title, author in books:
        assert isinstance(title, str)
        assert isinstance(author, str)
        assert title
        assert author


def test_first_three_books_slice():
    books = favorite_books()
    first = first_three_books(books)
    assert first == books[:3]
    assert len(first) == 3


def test_student_db_basic_ops():
    db = student_db()
    assert isinstance(db, dict)
    assert db["Joe Schmoe"] == 1
    assert get_student_id(db, "John Doe") == 2
    assert get_student_id(db, "Missing Person") is None
