"""
user_int_tests

Holds test cases that specifically test the `UserInt` and `ExtendedUserInt` classes.
"""

from math import trunc, floor, ceil, log2
from unittest import TestCase, main
from random import randrange
from ..userint import UserInt, ExtendedUserInt


class UserIntTests(TestCase):
    """
    `UserIntTests`

    Tests for the `UserInt` class.
    """

    def test_x(self):
        """
        `test_x`

        Tests that the `x` property of `ExtendedUserInt`
        holds and maintains it's value properly with random values.
        """
        for _ in range(5000):
            v = randrange(-1000000000, 1000000000)
            self.assertEqual(UserInt(v).x, v)

    def test_compairson_opperators_int(self):
        """
        `test_compairson_opperators_int`

        Tests that all the compairson opperators of `ExtendedUserInt`
        behaves as expected with random values.
        """

        for _ in range(5000):
            v1 = randrange(-1000000000, 1000000000)
            v2 = randrange(-1000000000, 1000000000)
            xintobj1 = ExtendedUserInt(v1)

            self.assertTrue(xintobj1 == v1)
            self.assertFalse(xintobj1 != v1)

            self.assertFalse(xintobj1 > v1)
            self.assertTrue(xintobj1 >= v1)

            self.assertFalse(xintobj1 < v1)
            self.assertTrue(xintobj1 <= v1)

            self.assertEqual(xintobj1 == v2, v1 == v2)
            self.assertEqual(xintobj1 != v2, v1 != v2)
            self.assertEqual(xintobj1 > v2, v1 > v2)
            self.assertEqual(xintobj1 >= v2, v1 >= v2)
            self.assertEqual(xintobj1 < v2, v1 < v2)
            self.assertEqual(xintobj1 <= v2, v1 <= v2)

    def test_arithmetic_opperators_int(self):
        """
        `test_arithmetic_opperators_int`

        Tests that all the non-inline arithmetic opperators of `ExtendedUserInt`
        behaves as expected with random values.
        """

        for _ in range(5000):
            v1 = randrange(-1000000000, 1000000000)
            v2 = randrange(-1000000000, 1000000000)
            xintobj1 = ExtendedUserInt(v1)

            self.assertEqual(xintobj1 + v2, v1 + v2)
            self.assertIsInstance(xintobj1 + v2, int)
            self.assertEqual(xintobj1 - v2, v1 - v2)
            self.assertIsInstance(xintobj1 - v2, int)
            self.assertEqual(xintobj1 * v2, v1 * v2)
            self.assertIsInstance(xintobj1 * v2, int)
            self.assertEqual(xintobj1 / v2, v1 / v2)
            self.assertIsInstance(xintobj1 / v2, (int, float))
            self.assertEqual(xintobj1 // v2, v1 // v2)
            self.assertIsInstance(xintobj1 // v2, int)
            self.assertEqual(xintobj1 % v2, v1 % v2)
            self.assertIsInstance(xintobj1 % v2, int)
            self.assertEqual(xintobj1 ** (abs(v2)%5), v1 ** (abs(v2)%5))
            self.assertIsInstance(xintobj1 ** (abs(v2)%5), int)

            self.assertEqual(-xintobj1, -v1)
            self.assertIsInstance(-xintobj1, int)
            self.assertEqual(+xintobj1, +v1)
            self.assertIsInstance(+xintobj1, int)
            self.assertEqual(abs(xintobj1), abs(v1))
            self.assertIsInstance(abs(xintobj1), int)

    def test_binary_opperators_int(self):
        """
        `test_binary_opperators_int`

        Tests that all the non-inline binary opperators of `ExtendedUserInt`
        behaves as expected with random values.
        """

        for _ in range(5000):
            v1 = randrange(-1000000000, 1000000000)
            v2 = randrange(-1000000000, 1000000000)
            v3 = randrange(0, 5)
            xintobj1 = ExtendedUserInt(v1)

            self.assertEqual(~xintobj1, ~v1)
            self.assertIsInstance(~xintobj1, int)
            self.assertEqual(xintobj1 & v2, v1 & v2)
            self.assertIsInstance(xintobj1 & v2, int)
            self.assertEqual(xintobj1 | v2, v1 | v2)
            self.assertIsInstance(xintobj1 | v2, int)
            self.assertEqual(xintobj1 ^ v2, v1 ^ v2)
            self.assertIsInstance(xintobj1 ^ v2, int)
            self.assertEqual(xintobj1 << v3, v1 << v3)
            self.assertIsInstance(xintobj1 << v3, int)
            self.assertEqual(xintobj1 >> v3, v1 >> v3)
            self.assertIsInstance(xintobj1 >> v3, int)

    def test_rounding_opperators_int(self):
        """
        `test_rounding_opperators_int`

        Tests that all the rounding opperators of `ExtendedUserInt`
        behaves as expected with random values.
        """

        for _ in range(5000):
            v1 = randrange(-1000000000, 1000000000)
            v2 = randrange(0, 5)
            xintobj1 = ExtendedUserInt(v1)

            self.assertEqual(trunc(xintobj1), trunc(v1))
            self.assertIsInstance(trunc(xintobj1), int)
            self.assertEqual(floor(xintobj1), floor(v1))
            self.assertIsInstance(floor(xintobj1), int)
            self.assertEqual(ceil(xintobj1), ceil(v1))
            self.assertIsInstance(ceil(xintobj1), int)
            self.assertEqual(round(xintobj1), round(v1))
            self.assertIsInstance(round(xintobj1), int)
            self.assertEqual(round(xintobj1, v2), round(v1, v2))
            self.assertIsInstance(round(xintobj1, v2), int)

    def test_conversion_opperators_int(self):
        """
        `test_conversion_opperators_int`

        Tests that all the type conversion opperators of `ExtendedUserInt`
        behaves as expected with random values.
        """

        for _ in range(5000):
            v1 = randrange(-100000, 100000)
            byte_len = ceil(log2(abs(v1)) / 8) + 1 # +1 for an extra spot to hold the sign bit
            xintobj1 = ExtendedUserInt(v1)

            self.assertEqual(int(xintobj1), int(v1))
            self.assertIsInstance(int(xintobj1), int)
            self.assertEqual(bool(xintobj1), bool(v1))
            self.assertIsInstance(bool(xintobj1), bool)
            self.assertEqual(xintobj1.to_bytes(byte_len, "big", signed = True),
                             v1.to_bytes(byte_len, "big", signed = True)
                             )
            self.assertIsInstance(xintobj1.to_bytes(byte_len, "big", signed = True), bytes)
            self.assertEqual(float(xintobj1), float(v1))
            self.assertIsInstance(float(xintobj1), float)
            self.assertEqual(str(xintobj1), str(v1))
            self.assertIsInstance(str(xintobj1), str)
            self.assertEqual(f"{xintobj1}", f"{v1}")
            self.assertIsInstance(f"{xintobj1}", str)
            self.assertEqual(f"{xintobj1:04X}", f"{v1:04X}")
            self.assertIsInstance(f"{xintobj1:04X}", str)
            self.assertEqual(complex(xintobj1), complex(v1))
            self.assertIsInstance(complex(xintobj1), complex)

    def test_hashing_opperators_int(self):
        """
        `test_hashing_opperators_int`

        Tests that all the hashing opperators of `ExtendedUserInt`
        behaves as expected with random values.
        """

        for _ in range(5000):
            v1 = randrange(-1000000000, 1000000000)
            xintobj1 = ExtendedUserInt(v1)

            self.assertEqual(hash(xintobj1), hash(v1))


class ExtendedUserIntTests(TestCase):
    """
    `ExtendedUserIntTests`

    Tests for the `ExtendedUserInt` class.
    """

    def test_sign(self):
        """
        `test_sign`

        Tests that the `sign` property of `ExtendedUserInt`
        behaves as expected with random values.
        """
        for _ in range(5000):
            v = randrange(-1000000000, 1000000000)
            vsign = 0 if v == 0 else (-1 if v < 0 else 1)
            self.assertEqual(ExtendedUserInt(v).sign, vsign)


if __name__ == '__main__':
    main()
