
import unittest

from src.pcm import quantize_samples


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


if __name__ == "__main__":
    unittest.main()
