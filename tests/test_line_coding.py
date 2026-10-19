
import unittest

from src.line_coding import (
    encode_nrz_l,
    encode_nrz_i,
    encode,
    encode_manchester,
encode_differential_manchester,
)


class TestLineCoding(unittest.TestCase):

    def test_nrz_l(self):
        self.assertEqual(
            encode_nrz_l("10110"),
            [1, -1, 1, 1, -1],
        )

    def test_nrz_i(self):
        self.assertEqual(
            encode_nrz_i("10110"),
            [1, 1, -1, 1, 1],
        )

    def test_nrz_i_custom_initial_level(self):
        self.assertEqual(
            encode_nrz_i("10", initial_level=1),
            [-1, -1],
        )

    def test_manchester(self):
        self.assertEqual(
            encode_manchester("010"),
            [1, -1, -1, 1, 1, -1],
        )

    def test_differential_manchester(self):
        self.assertEqual(
            encode_differential_manchester("01"),
            [-1, 1, 1, -1],
        )

    def test_manchester_invalid_bits(self):
        with self.assertRaises(ValueError):
            encode_manchester("10x")

    def test_differential_manchester_invalid_level(self):
        with self.assertRaises(ValueError):
            encode_differential_manchester("101", initial_level=0)

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            encode_nrz_l("")

    def test_invalid_bits(self):
        with self.assertRaises(ValueError):
            encode_nrz_i("10201")

    def test_invalid_initial_level(self):
        with self.assertRaises(ValueError):
            encode_nrz_i("101", initial_level=0)

    def test_registry(self):
        self.assertEqual(encode("10", "NRZ-L"), [1, -1])

    def test_unknown_scheme(self):
        with self.assertRaises(ValueError):
            encode("101", "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
