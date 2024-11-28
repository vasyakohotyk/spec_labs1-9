"""
This module provides a function to convert a given integer into a list of powers of two,
representing the binary breakdown of the integer.
"""


def int_to_bit_powers(n):
    """
    Convert an integer into a list of powers of two.

    :param n: An integer to convert into a list of powers of two.
     The input should be a non-negative integer.
    :return: A list of integers where each integer is a power of two
     that sums up to the input integer when combined. The result list
     will represent the binary breakdown of the input integer.
    """
    result = []
    power = 0
    while n > 0:
        if n & 1:
            result.append(2 ** power)
        n >>= 1
        power += 1
    return result
