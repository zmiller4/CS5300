import pytest

from task4 import calculate_discount


@pytest.mark.parametrize(
    "price,discount,expected",
    [
        (100, 0, 100.0),
        (100, 10, 90.0),
        (200, 50, 100.0),
        (19.99, 25, 14.9925),
        (19.99, 12.5, 17.49125),
        (0, 80, 0.0),
    ],
)
def test_calculate_discount_numeric_types(price, discount, expected):
    assert calculate_discount(price, discount) == pytest.approx(expected)


def test_calculate_discount_rejects_non_numeric():
    with pytest.raises(TypeError):
        calculate_discount("100", 10)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        calculate_discount(100, "10")  # type: ignore[arg-type]


@pytest.mark.parametrize("price", [-1, -0.01])
def test_calculate_discount_rejects_negative_price(price):
    with pytest.raises(ValueError):
        calculate_discount(price, 10)


@pytest.mark.parametrize("discount", [-1, 101, 100.0001])
def test_calculate_discount_rejects_invalid_discount(discount):
    with pytest.raises(ValueError):
        calculate_discount(100, discount)
