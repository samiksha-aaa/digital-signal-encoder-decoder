
import unittest

from src.decoder import (
    decode_nrz_l,
    decode_nrz_i,
    decode_manchester,
    decode_differential_manchester,
    decode_ami,
    decode_b8zs,
    decode_hdb3,
)


class TestDecoder(unittest.TestCase):

    def test_nrz_l(self):
        self.assertEqual(decode_nrz_l([1, -1, 1, 1, -1]), "10110")

    def test_nrz_i(self):
        self.assertEqual(decode_nrz_i([-1, 1, 1, -1]), "0101")

    def test_nrz_l_empty_signal(self):
        with self.assertRaises(ValueError):
            decode_nrz_l([])

    def test_nrz_i_empty_signal(self):
        with self.assertRaises(ValueError):
            decode_nrz_i([])

    def test_manchester(self):
        self.assertEqual(
            decode_manchester([1, -1, -1, 1, 1, -1]),
            "010",
        )

    def test_differential_manchester(self):
        self.assertEqual(
            decode_differential_manchester(
                [-1, 1, 1, -1, -1, 1],
                initial_level=1,
            ),
            "011",
        )

    def test_ami(self):
        self.assertEqual(decode_ami([1, 0, -1, 1, 0]), "10110")

    def test_ami_invalid_level(self):
        with self.assertRaises(ValueError):
            decode_ami([1, 2, 0])

    def test_b8zs(self):
        signal = [1, 0, 0, 0, 1, -1, 0, -1, 1]
        self.assertEqual(decode_b8zs(signal), "100000000")

    def test_hdb3_odd_pulse_count(self):
        signal = [1, 0, 0, 0, 1]
        self.assertEqual(decode_hdb3(signal), "10000")

    def test_hdb3_even_pulse_count(self):
        signal = [1, -1, 1, 0, 0, 1]
        self.assertEqual(decode_hdb3(signal), "110000")

    def test_scrambling_decoders_reject_empty_input(self):
        with self.assertRaises(ValueError):
            decode_b8zs([])

        with self.assertRaises(ValueError):
            decode_hdb3([])

    def test_b8zs_round_trip(self):
        from src.scrambling import encode_b8zs

        bits = "100000000"
        signal = encode_b8zs(bits)
        self.assertEqual(decode_b8zs(signal), bits)

    def test_hdb3_round_trip(self):
        from src.scrambling import encode_hdb3

        bits = "10000"
        signal = encode_hdb3(bits)
        self.assertEqual(decode_hdb3(signal), bits)

    def test_hdb3_multiple_zero_sequences(self):
        from src.scrambling import encode_hdb3

        bits = "1000010000"
        signal = encode_hdb3(bits)
        self.assertEqual(decode_hdb3(signal), bits)


if __name__ == "__main__":
    unittest.main()
