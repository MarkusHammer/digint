"""
digint_tests

Holds test cases that specifically test the `digitint` class and it's capabilities.
"""

from unittest import TestCase, main
from random import randrange
from ..digint import digitint
from ..tools import absindex


class DigitintPreset(TestCase):
    """
    `DigitintPreset`

    Tests the `digitint` class and it's capabilities using a contant collection of preset examples.
    """
    CONSTS = (
        {
            "whole" : 54321,
            "base" : 10,
            "index" : 1,
            "popped" : 2,
            "remainder" : 5431
        },
        {
            "whole" : 87654321,
            "base" : 10,
            "index" : -1,
            "popped" : 8,
            "remainder" : 7654321
        },
        {
            "whole" : 7654321,
            "base" : 10,
            "index" : 5,
            "popped" : 6,
            "remainder" : 754321
        },
        {
            "whole" : 987654321,
            "base" : 10,
            "index" : slice(3,6),
            "popped" : [4,5,6],
            "remainder" : 987321
        },
        {
            "whole" : 0xABCDEF,
            "base" : 16,
            "index" : 3,
            "popped" : 0xC,
            "remainder" : 0xABDEF
        },
        {
            "whole" : 0xABCDEF,
            "base" : 16,
            "index" : -1,
            "popped" : 0xA,
            "remainder" : 0xBCDEF
        },
        {
            "whole" : "ABCDEF",
            "base" : 23,
            "index" : -1,
            "popped" : int("A", 23),
            "remainder" : int("BCDEF", 23)
        },
        {
            "whole" : "ABCDEF",
            "base" : 36,
            "index" : 4,
            "popped" : int("B", 36),
            "remainder" : int("ACDEF", 36)
        },
        {
            "whole" : ["5",4,3,"2",1],
            "base" : 10,
            "index" : 1,
            "popped" : 2,
            "remainder" : 5431
        },
        {
            "whole" : bytes([5,4,3,2,1]),
            "base" : 10,
            "index" : 1,
            "popped" : 2,
            "remainder" : 5431
        }
    )

    def test_get(self):
        """
        `test_get`

        Tests that the `digitint` class's `__getitem__` behaves as expected
        using the tests case's contant examples.
        """
        for test_set in self.CONSTS:
            gotten = digitint(test_set["whole"], test_set["base"]).get_digit(test_set["index"])
            self.assertEqual(gotten, test_set["popped"])

    def test_set(self):
        """
        `test_set`

        Tests that the `digitint` class's `__setitem__` behaves as expected
        using the tests case's contant examples.
        """
        for test_set in self.CONSTS:
            dintobj = digitint(test_set["whole"], test_set["base"])
            newval = randrange(0, dintobj.base - 1)
            dintobj[2] = newval
            self.assertEqual(dintobj[2], newval)

    def test_del(self):
        """
        `test_del`

        Tests that the `digitint` class's `__delitem__` behaves as expected
        using the tests case's contant examples.
        """
        for test_set in self.CONSTS:
            o = digitint(test_set["whole"], test_set["base"])
            del o[test_set["index"]]
            self.assertEqual(int(o), test_set["remainder"])

    def test_mask(self):
        """
        `test_mask`

        Tests that the `digitint` class's `mask` behaves as expected
        using the tests case's contant examples.
        """
        for test_set in self.CONSTS:
            if not isinstance(test_set["index"], int):
                continue
            dintobj = digitint(test_set["whole"], test_set["base"])
            expected_mask = test_set["popped"]
            expected_mask *= (dintobj.base ** absindex(test_set["index"], dintobj.digit_length()))
            self.assertEqual(dintobj.mask(test_set["index"]), expected_mask)

    def test_insert(self):
        """
        `test_insert`

        Tests that the `digitint` class's `insert` behaves as expected
        using the tests case's contant examples.
        """

        for test_set in self.CONSTS:
            if not isinstance(test_set["index"], int):
                continue

            expected_result = digitint(test_set["whole"], test_set["base"])
            inserted = digitint(test_set["remainder"], test_set["base"])
            inserted.insert(test_set["index"], test_set["popped"])
            self.assertEqual(expected_result, inserted)


class DigitintRandom(TestCase):
    """
    `DigitintRandom`

    Tests the `digitint` class and it's capabilities using randomly generated example values.
    """
    def test_digit_length_decimal(self):
        """
        `test_digit_length_decimal`

        Tests that the `digitint` class's `digit_length` behaves as expected
        with random values in base 10.
        """
        for _ in range(50000):
            val = randrange(-1000000, 1000000)
            diglen = digitint(val, 10).digit_length()
            if val == 0:
                self.assertEqual(diglen, 0)
            else:
                self.assertEqual(diglen, len(str(abs(val))))

    def test_digit_length_hex(self):
        """
        `test_digit_length_hex`

        Tests that the `digitint` class's `digit_length` behaves as expected
        with random values in base 16.
        """
        for _ in range(50000):
            val = randrange(-1000000, 1000000)
            diglen = digitint(val, 16).digit_length()
            if val == 0:
                self.assertEqual(diglen, 0)
            else:
                self.assertEqual(diglen, len(hex(abs(val)).lstrip("0x")))

    def test_digit_length_bin(self):
        """
        `test_digit_length_bin`

        Tests that the `digitint` class's `digit_length` behaves as expected
        with random values in base 2.
        """
        for _ in range(50000):
            val = randrange(-1000000, 1000000)
            diglen = digitint(val, 2).digit_length()
            self.assertEqual(diglen, val.bit_length())
            if val == 0:
                self.assertEqual(diglen, 0)
            else:
                self.assertEqual(diglen, len(bin(abs(val)).lstrip("0b")))

    def test_digit_length_oct(self):
        """
        `test_digit_length_oct`

        Tests that the `digitint` class's `digit_length` behaves as expected
        with random values in base 8.
        """
        for _ in range(50000):
            val = randrange(-1000000, 1000000)
            diglen = digitint(val, 8).digit_length()
            if val == 0:
                self.assertEqual(diglen, 0)
            else:
                self.assertEqual(diglen, len(oct(abs(val)).lstrip("0o")))

    def test_digit_length_unary(self):
        """
        `test_digit_length_unary`

        Tests that the `digitint` class's `digit_length` behaves as expected
        with random values in base 1.
        """
        for _ in range(50000):
            val = randrange(-1000000, 1000000)
            diglen = digitint(val, 1).digit_length()
            self.assertEqual(diglen, abs(val))
            if val == 0:
                self.assertEqual(diglen, 0)


if __name__ == '__main__':
    main()
