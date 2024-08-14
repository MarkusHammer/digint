"""
digint_tests

Holds test cases that specifically test the `digitint` class and it's capabilities.
"""

import unittest
from random import randrange
from ..digint import digitint
from ..tools import absindex

class DigintPreset(unittest.TestCase):
    """
    `DigintPreset`
    
    Tests the `digint` class and it's capabilities using a contant collection of preset examples.
    """
    #formated as (source_int, source_base) : (popped_value, popping_index, remaining_int)
    CONSTS = {
        (987654321, 10) : (2, 1, 98765431),
        (987654321, 10) : (9, -1, 87654321),
        (987654321, 10) : (6, 5, 98754321),
        (987654321, 10) : ([4,5,6], slice(3,6), 987321),
        (0xABCDEF, 16) : (0xC, 3, 0xABDEF),
        (0xABCDEF, 16) : (0xA, -1, 0xBCDEF),
        ("ABCDEF", 23) : (int("A", 23), -1, int("BCDEF", 23)),
        ("ABCDEF", 36) : (int("B", 36), 4, int("ACDEF", 36))
    }

    def test_get(self):
        """
        `test_get`
        
        Tests that the `digint` class's `__getitem__` behaves as expected
        using the tests case's contant examples.
        """
        for inv, outv in self.CONSTS.items():
            self.assertEqual(digitint(*inv).get_digit(outv[1]), outv[0])

    def test_set(self):
        """
        `test_set`
        
        Tests that the `digint` class's `__setitem__` behaves as expected
        using the tests case's contant examples.
        """
        for inv in self.CONSTS:
            dintobj = digitint(*inv)
            newval = randrange(0, dintobj.base - 1)
            dintobj[2] = newval
            self.assertEqual(dintobj[2], newval)

    def test_del(self):
        """
        `test_del`
        
        Tests that the `digint` class's `__delitem__` behaves as expected
        using the tests case's contant examples.
        """
        for inv, outv in self.CONSTS.items():
            o = digitint(*inv)
            del o[outv[1]]
            self.assertEqual(int(o), outv[2])

    def test_mask(self):
        """
        `test_mask`
        
        Tests that the `digint` class's `mask` behaves as expected
        using the tests case's contant examples.
        """
        for inv, outv in self.CONSTS.items():
            if not isinstance(outv[1], int):
                continue
            dintobj = digitint(*inv)
            expected_mask = outv[0] * (dintobj.base ** absindex(outv[1], dintobj.digit_length()))
            self.assertEqual(dintobj.mask(outv[1]), expected_mask)

class DigintRandom(unittest.TestCase):
    """
    `DigintRandom`
    
    Tests the `digint` class and it's capabilities using randomly generated example values.
    """
    def test_digit_length_decimal(self):
        """
        `test_digit_length_decimal`
        
        Tests that the `digint` class's `digit_length` behaves as expected
        with random values in base 10.
        """
        for _ in range(5000):
            val = randrange(-1000000, 1000000)
            self.assertEqual(digitint(val, 10).digit_length(), len(str(abs(val))))

    def test_digit_length_hex(self):
        """
        `test_digit_length_hex`
        
        Tests that the `digint` class's `digit_length` behaves as expected
        with random values in base 16.
        """
        for _ in range(5000):
            val = randrange(-1000000, 1000000)
            self.assertEqual(digitint(val, 16).digit_length(), len(hex(abs(val)).lstrip("0x")))

    def test_digit_length_bin(self):
        """
        `test_digit_length_bin`
        
        Tests that the `digint` class's `digit_length` behaves as expected
        with random values in base 2.
        """
        for _ in range(5000):
            val = randrange(-1000000, 1000000)
            self.assertEqual(digitint(val, 2).digit_length(), val.bit_length())
            self.assertEqual(digitint(val, 2).digit_length(), len(bin(abs(val)).lstrip("0b")))

    def test_digit_length_oct(self):
        """
        `test_digit_length_oct`
        
        Tests that the `digint` class's `digit_length` behaves as expected
        with random values in base 8.
        """
        for _ in range(5000):
            val = randrange(-1000000, 1000000)
            self.assertEqual(digitint(val, 8).digit_length(), len(oct(abs(val)).lstrip("0o")))

if __name__ == '__main__':
    unittest.main()
