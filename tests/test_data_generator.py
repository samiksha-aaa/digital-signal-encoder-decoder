
import unittest

from src.data_generator import (
    generate_random_bits,
    generate_bits_with_zeros,
    longest_palindrome,
)


class TestDataGenerator(unittest.TestCase):

    def test_random_bits(self):
        bits = generate_random_bits(100)
        self.assertEqual(len(bits), 100)
        self.assertTrue(set(bits) <= {"0", "1"})

    def test_fixed_four_zeros(self):
        bits = generate_bits_with_zeros(30, 4)
        self.assertEqual(len(bits), 30)
        self.assertIn("0000", bits)

    def test_fixed_eight_zeros(self):
        bits = generate_bits_with_zeros(30, 8)
        self.assertEqual(len(bits), 30)
        self.assertIn("00000000", bits)

    def test_palindrome(self):
        self.assertEqual(
            longest_palindrome("1101001011"),
            "1101001011"
        )

    def test_entire_string_palindrome(self):
        self.assertEqual(longest_palindrome("10101"), "10101")

    def test_empty_string(self):
        self.assertEqual(longest_palindrome(""), "")

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            generate_random_bits(0)


if __name__ == "__main__":
    unittest.main()
