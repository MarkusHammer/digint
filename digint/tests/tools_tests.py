"""
tools_tests

Holds test cases that specifically test the functions defined in `tools`.
"""

import unittest
from random import randrange
from ..tools import absindex

class AbsIndexTests(unittest.TestCase):
    """
    `AbsIndexTests`

    Tests the `absindex` tool function.
    """

    def test_random_range(self):
        """
        `test_random_range`
        
        Tests that `absindex` return roughly sane values with random inputs.
        """

        for _ in range(5000):
            length = randrange(1, 1000000)

            index = randrange(-(length + 1), length)
            absind = absindex(index, length)
            self.assertGreaterEqual(absind, 0)
            self.assertLess(absind, length)

    def test_random_range_drifting(self):
        """
        `test_random_range_drifting`
        
        Similar to `test_random_range`, but repeatedly tests that a random value,
        when fed back into `absindex` returns the same index.
        """

        for _ in range(500):
            length = randrange(1, 1000000)
            index = randrange(-(length + 1), length)
            absind = absindex(index, length)
            for _ in range(randrange(5, 10)):
                temp_absind = absindex(absind, length)
                self.assertEqual(absind, temp_absind)
                absind = temp_absind

    def test_positive_index(self):
        """
        `test_positive_index`
        
        Ensures that positive indexes are properly preserved
        when inputted.
        """
        for _ in range(5000):
            length = randrange(1, 1000000)
            index = randrange(0, length)
            absind = absindex(index, length)
            self.assertEqual(absind, index)

    def test_negative_index(self):
        """
        `test_negative_index`
        
        Ensures that negative indexes are properly converted
        to their positive counterpart with `absindex` by using random values.
        """

        for _ in range(5000):
            length = randrange(1, 1000000)
            index = randrange(-length, -1)
            absind = absindex(index, length)
            self.assertEqual(absind, length + index)

if __name__ == '__main__':
    unittest.main()
