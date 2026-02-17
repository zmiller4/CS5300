"""
Task 3: Control Structures
"""
from __future__ import annotations
from typing import List

def classify_number(n: float) -> str:
    if n > 0:
        return "positive"
    if n < 0:
        return "negative"
    return "zero"

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Check if n is divisible by odd numbers 
    # Only check for values of d that are less than sqrt(n)
    # If n has a factor that is > sqrt(n), then its 
    # corresponding factor would have been < sqrt(n) and 
    # we would've already found it.
    d = 3
    while d * d <= n: # faster than d <= math.isqrt(n)
        if n % d == 0:
            return False
        d += 2
    return True

def first_n_primes(count: int) -> List[int]:
    if count < 0:
        raise ValueError("count must be >= 0")
    primes: List[int] = []
    candidate = 2
    while len(primes) < count:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes

def sum_1_to_n(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    total = 0
    i = 1
    while i <= n:
        total += i
        i += 1
    return total

def first_10_primes() -> List[int]:
    return first_n_primes(10)

def sum_1_to_100() -> int:
    return sum_1_to_n(100)
