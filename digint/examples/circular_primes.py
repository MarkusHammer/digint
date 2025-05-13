"""
Circular Primes

This module holds functions used to generate and check for circular primes using digint.
"""

from itertools import combinations_with_replacement
from math import gcd
from typing import Generator
from sympy import isprime
from ..digint import digitint


def notate_digit_value(digit_value:int, base:int) -> str:
    """
    Convert a digit value to its string representation in a given base.

    Args:
        digit_value (int): The digit value to be converted.
        base (int): The numerical base for conversion.

    Returns:
        str: The string representation of the digit value in the given base.
    """

    return str(digitint(digit_value, base))


def coprime(*values:int, include_naught_and_unity:bool = False) -> bool:
    """
    Check if all values are coprime.

    Args:
        *values (int): The values to be checked for coprimality.
        include_naught_and_unity (bool): Include 0 and 1 as valid values
            when checking for coprimality. Defaults to False.

    Returns:
        bool: A boolean indicating if all values are coprime.
    """
    if not include_naught_and_unity and (1 in values or 0 in values):
        return False
    return gcd(*values) in (0,1)
    # One or zero, but not negative one or anything below,
    # as -1 is a factor for all negative numbers


def is_repunit(number: digitint) -> bool:
    """
    Check if a number is a repunit
    (a number where all digits are unity, ex. 111 or 1111111).

    Args:
        number (digitint): The number to be checked.

    Returns:
        bool: A boolean indicating if the number is a repunit.
    """
    if number == 0 or number[0] != 1:
        return False
    shift_number = number.copy()
    shift_number.digit_rotate_left(1)
    return number == shift_number


def is_circularly_prime(number:digitint) -> bool:
    """
    Check if a number is a circular prime.
    Generally, this is faster to run for when false than when true.

    Args:
        number (digitint): The number to be checked.

    Returns:
        bool: A boolean indicating if the number is a circular prime.
    """
    if len(number) < 2 or is_repunit(number):
        return isprime(number)
    number.digit_rotate_left()  # rotate once to have the final value rotated to the original
    started:int = int(number)
    for _ in range(len(number)):
        number.digit_rotate_left()
        if not isprime(int(number)):  # if its not prime now, its not a circular prime ever
            return False
        if started == int(number):  # the number repeats rotationally, so no need to continue
            break
    return True


def circular_primes(amount_of_digits:int = 2, base:int = 10) -> Generator[digitint, None, None]:
    """
    Generate circular primes in a given base.

    Args:
        amount_of_digits (int): The amount of digits to generate circular primes with.
        base (int): The numerical base to generate circular primes with.

    Yields:
        digitint: A circular prime number in the given base.
    """
    if base == 2:  # Trivial to handle on a binary computer, its just a Mersenne prime...
        val:int = (1 << amount_of_digits) - 1
        if isprime(val):
            yield digitint(val, base)
    elif amount_of_digits == 1:  # This is just all one digit primes...
        yield from (digitint(d, base) for d in range(2, base) if isprime(d))  # just return all one digit primes
    else:
        # A generates a list of digits that don't make the number composite when in the units spot
        # (ex. in base 10, all digits except 0, 2, 4, 5, 6 or 8; aka only the digits 1,3,7,9)
        possible_digits = (x for x in range(1, base, 0 if base % 2 else 2) if coprime(base, x, include_naught_and_unity=True))
        for combo in combinations_with_replacement(possible_digits, amount_of_digits):
            combo = digitint(combo, base)
            if is_circularly_prime(combo):
                yield combo


if __name__ == "__main__":
    from sys import argv, exit as sysexit
    from argparse import ArgumentParser

    parser = ArgumentParser(argv.pop(0))
    parser.add_argument("maxdigitcount", type = int)
    parser.add_argument("base", type = int, default=10)
    parser.add_argument("--noduplicates", "-q", "--quiet", "--nodupe", action="store_true")
    parsed = parser.parse_args(argv)

    # The following is made in such a way that the printing of the found values to stdout is done immediately when the number is found, to give a sense of time to the algorithm.
    # This is why things like ```flush``` and all the ansi codes are used to manipulate the printed contents here.

    try:
        for digit_amount in range(1, parsed.maxdigitcount+1):
            print(f"{digit_amount} : []", end = "", flush=True)  # initialize the line's contents
            first:bool = True  # is this the first prime found?
            for n in circular_primes(digit_amount, parsed.base):
                print(f"\b{str(n)}]" if first else f"\b, {str(n)}]",  # `\b` is used to delete the last character printed.
                      end = "",
                      flush=True
                      )  # print the prime with the proper pattern.
                first = False
            print('\x1b[2K\r' if first and parsed.noduplicates else "\n",
                  end="")
            # if there was no first found number,
            # either delete the last line or make a new line depending on the argument
    except KeyboardInterrupt:
        pass  # don't sweat the keaboard interupts, those arn't really errors,
              # just the user getting bored
    sysexit(0)
