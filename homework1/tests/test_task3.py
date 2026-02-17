import pytest

from task3 import (
    classify_number,
    first_10_primes,
    first_n_primes,
    is_prime,
    sum_1_to_100,
    sum_1_to_n,
)


@pytest.mark.parametrize(
    "n,expected",
    [
        (5, "positive"),
        (0, "zero"),
        (-3, "negative"),
        (0.0, "zero"),
        (-0.0, "zero"),
        (1e-12, "positive"),
        (-1e-12, "negative"),
    ],
)
def test_classify_number(n, expected):
    assert classify_number(n) == expected


@pytest.mark.parametrize(
    "n,expected",
    [
        (-1, False),
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (9, False),
        (29, True),
        (49, False),
    ],
)
def test_is_prime(n, expected):
    assert is_prime(n) is expected


def test_first_10_primes():
    assert first_10_primes() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


@pytest.mark.parametrize(
    "count,expected",
    [
        (0, []),
        (1, [2]),
        (2, [2, 3]),
        (5, [2, 3, 5, 7, 11]),
    ],
)
def test_first_n_primes(count, expected):
    assert first_n_primes(count) == expected


def test_first_n_primes_negative_count():
    with pytest.raises(ValueError):
        first_n_primes(-1)


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, 0),
        (1, 1),
        (2, 3),
        (10, 55),
        (100, 5050),
    ],
)
def test_sum_1_to_n(n, expected):
    assert sum_1_to_n(n) == expected


def test_sum_1_to_n_negative():
    with pytest.raises(ValueError):
        sum_1_to_n(-1)


def test_sum_1_to_100():
    assert sum_1_to_100() == 5050
