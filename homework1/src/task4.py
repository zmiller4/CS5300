"""
Task 4: Functions and Duck Typing
"""

from __future__ import annotations
from numbers import Real

def calculate_discount(price: Real, discount: Real) -> float:
    if not isinstance(price, Real) or not isinstance(discount, Real):
        raise TypeError("price and discount must be numeric")
    if price < 0:
        raise ValueError("price must be >= 0")
    if discount < 0 or discount > 100:
        raise ValueError("discount must be between 0 and 100")
    return float(price) * (1.0 - (float(discount) / 100.0))

def main() -> None:
    examples = [
        (100, 0),
        (100, 15),
        (49.99, 20),
        (250, 50),
    ]

    for price, discount in examples:
        final_price = calculate_discount(price, discount)
        print(f"price={price}, discount={discount}% -> {final_price:.2f}")

if __name__ == "__main__":
    main()