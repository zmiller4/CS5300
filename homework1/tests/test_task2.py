import pytest

from task2 import (
    add_integers,
    concat_strings,
    divide_floats,
    sample_values,
    toggle_boolean,
)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (0, 0, 0),
        (1, 2, 3),
        (-5, 10, 5),
    ],
)
def test_add_integers(a, b, expected):
    result = add_integers(a, b)
    assert isinstance(result, int)
    assert result == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1.0, 2.0, 0.5),
        (3.0, 2.0, 1.5),
        (-1.0, 4.0, -0.25),
    ],
)
def test_divide_floats(a, b, expected):
    result = divide_floats(a, b)
    assert isinstance(result, float)
    assert result == pytest.approx(expected)


def test_divide_floats_zero_division():
    with pytest.raises(ZeroDivisionError):
        divide_floats(1.0, 0.0)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        ("", "", ""),
        ("hello", "world", "helloworld"),
        ("a", " ", "a "),
    ],
)
def test_concat_strings(a, b, expected):
    result = concat_strings(a, b)
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (True, False),
        (False, True),
    ],
)
def test_toggle_boolean(value, expected):
    result = toggle_boolean(value)
    assert isinstance(result, bool)
    assert result is expected


def test_sample_values_types():
    data = sample_values()
    assert isinstance(data["count"], int)
    assert isinstance(data["ratio"], float)
    assert isinstance(data["label"], str)
    assert isinstance(data["enabled"], bool)
