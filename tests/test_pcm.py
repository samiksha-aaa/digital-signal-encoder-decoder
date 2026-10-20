
import unittest

from src.pcm import quantize_samples, encode_pcm , decode_pcm

class TestPCM(unittest.TestCase):

    def test_quantize_zero(self):
        result = quantize_samples([0.0], bits_per_sample=8)
        self.assertEqual(len(result), 1)
        self.assertTrue(-1.0 <= result[0] <= 1.0)

    def test_quantize_preserves_sample_count(self):
        samples = [-1.0, -0.5, 0.0, 0.5, 1.0]
        result = quantize_samples(samples)
        self.assertEqual(len(result), len(samples))

    def test_quantized_values_are_in_range(self):
        result = quantize_samples([-1.0, -0.2, 0.4, 1.0])
        for value in result:
            self.assertGreaterEqual(value, -1.0)
            self.assertLessEqual(value, 1.0)

    def test_invalid_empty_samples(self):
        with self.assertRaises(ValueError):
            quantize_samples([])

    def test_invalid_bits_per_sample(self):
        with self.assertRaises(ValueError):
            quantize_samples([0.5], bits_per_sample=0)

    def test_sample_out_of_range(self):
        with self.assertRaises(ValueError):
            quantize_samples([1.5])

    def test_more_bits_gives_finer_quantization(self):
        sample = [0.1234]
        low_resolution = quantize_samples(sample, bits_per_sample=2)
        high_resolution = quantize_samples(sample, bits_per_sample=8)

        self.assertLessEqual(
            abs(high_resolution[0] - sample[0]),
            abs(low_resolution[0] - sample[0]),
        )

    def test_encode_pcm_returns_binary_codewords(self):
        result = encode_pcm([-1.0, 0.0, 1.0], bits_per_sample=3)

        self.assertEqual(len(result), 3)
        for codeword in result:
            self.assertEqual(len(codeword), 3)
            self.assertTrue(set(codeword).issubset({"0", "1"}))

    def test_encode_pcm_saturation(self):
        result = encode_pcm([-1.0, 1.0], bits_per_sample=3)

        self.assertEqual(result, ["000", "111"])

    def test_encode_pcm_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            encode_pcm([])

    def test_encode_pcm_rejects_invalid_bit_depth(self):
        with self.assertRaises(ValueError):
            encode_pcm([0.5], bits_per_sample=0)

    def test_decode_pcm_returns_reconstructed_samples(self):
        codewords = ["000", "100", "111"]
        result = decode_pcm(codewords, bits_per_sample=3)

        self.assertEqual(result, [-0.875, 0.125, 0.875])

    def test_decode_pcm_round_trip(self):
        samples = [-1.0, -0.5, 0.0, 0.5, 1.0]
        codewords = encode_pcm(samples, bits_per_sample=8)
        reconstructed = decode_pcm(codewords, bits_per_sample=8)

        expected = quantize_samples(samples, bits_per_sample=8)
        self.assertEqual(reconstructed, expected)

    def test_decode_pcm_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            decode_pcm([])

    def test_decode_pcm_rejects_invalid_codeword(self):
        with self.assertRaises(ValueError):
            decode_pcm(["01X"], bits_per_sample=3)

    def test_decode_pcm_rejects_wrong_codeword_length(self):
        with self.assertRaises(ValueError):
            decode_pcm(["01"], bits_per_sample=3)

    def test_decode_pcm_rejects_invalid_bit_depth(self):
        with self.assertRaises(ValueError):
            decode_pcm(["000"], bits_per_sample=0)


if __name__ == "__main__":
    unittest.main()
