"""
happy_numbers.py

An example of using digint to generate happy numbers.
"""

from itertools import product, count
from ..digint import digitint


def happy_numbers(base=10):
    """
    Generate happy numbers in a given base.

    A happy number is a number defined by the following process:
    Starting with any positive integer, replace the number by the sum of the
    squares of its digits in the given base, and repeat the process until
    the number equals 1 (where it will stay), or it loops endlessly in a cycle
    which does not include 1. Those numbers for which this process ends in 1
    are happy numbers.

    Parameters:
    - base (int): The numerical base in which to find happy numbers.

    Yields:
    - digitint: A happy number in the specified base.
    """
    found = []
    for digit_count in count(start = 1):
        for combo in product(range(base), repeat=digit_count):
            combo = digitint(combo, base)
            combo_no_zeros = combo.copy()
            while combo_no_zeros != 0 and combo_no_zeros[0] == 0:
                del combo_no_zeros[0]

            if int(combo) in found:
                continue
            elif int(combo_no_zeros) in found and int(combo) not in found:
                found.append(int(combo))
                yield combo

            sqr_summed = 0
            for digit in combo:
                sqr_summed += digit * digit
            if sqr_summed == 1 and (int(combo) not in found):
                found.append(int(combo))
                yield combo
            sqr_summed_zero_removed = digitint(sqr_summed, base)
            while sqr_summed_zero_removed != 0 and sqr_summed_zero_removed[0] == 0:
                del sqr_summed_zero_removed[0]
            if (sqr_summed in found or int(sqr_summed_zero_removed) in found) and int(combo) not in found:
                found.append(int(combo))
                yield combo


def __main__(_progname:str, *args:str) -> int:
    """
    Main function to happily generate numbers.

    Returns the exit status of the program.
    """
    base = int(args[0]) if len(args) > 0 else 10
    for n in happy_numbers(base):
        print(digitint(n, base))
    return 0


if __name__ == "__main__":
    from sys import argv, exit as sysexit
    sysexit(__main__(*argv))
