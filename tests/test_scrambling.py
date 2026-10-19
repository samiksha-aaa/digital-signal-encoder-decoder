
import unittest

from src.scrambling import (
    encode_ami,
    encode_b8zs,
    encode_hdb3,
)


class TestScrambling(unittest.TestCase):

    def test_ami(self):
        self.assertEqual(
            encode_ami("11010"),
            [1, -1, 0, 1, 0],
        )

    def test_b8zs_positive_previous_pulse(self):
        self.assertEqual(
            encode_b8zs("100000000"),
            [1, 0, 0, 0, 1, -1, 0, -1, 1],
        )

    def test_b8zs_negative_previous_pulse(self):
        self.assertEqual(
            encode_b8zs("1100000000"),
            [1, -1, 0, 0, 0, -1, 1, 0, 1, -1],
        )

    def test_hdb3_odd_pulse_count(self):
        self.assertEqual(
            encode_hdb3("10000"),
            [1, 0, 0, 0, 1],
        )

    def test_hdb3_even_pulse_count(self):
        self.assertEqual(
            encode_hdb3("110000"),
            [1, -1, 1, 0, 0, 1],
        )

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            encode_b8zs("10x01")

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            encode_hdb3("")


if __name__ == "__main__":
    unittest.main()
