import math


def gcd(a, b):
    """
    The greatest common divisor (gcd) of two or more integers, which are not all zero,
    is the largest positive integer that divides each of the integers
    """
    if b == 0:
        return a
    else:
        d = a - b * math.floor(a / b)
        return gcd(b, d)
