
def quantize_samples(
    samples: list[float],
    bits_per_sample: int = 8,
) -> list[float]:
    """Quantize input samples to discrete PCM amplitude levels."""
    if not samples:
        raise ValueError("Samples cannot be empty.")

    if bits_per_sample < 1 or bits_per_sample > 16:
        raise ValueError("bits_per_sample must be between 1 and 16.")

    if any(not isinstance(sample, (int, float)) for sample in samples):
        raise ValueError("All samples must be numeric.")

    if any(not -1.0 <= sample <= 1.0 for sample in samples):
        raise ValueError("Samples must be between -1.0 and 1.0.")

    levels = 2**bits_per_sample
    step_size = 2.0 / levels

    quantized = []

    for sample in samples:
        index = int((sample + 1.0) / step_size)
        index = min(index, levels - 1)

        representative = -1.0 + (index + 0.5) * step_size
        quantized.append(round(representative, 6))

    return quantized


def encode_pcm(
    samples: list[float],
    bits_per_sample: int = 8,
) -> list[str]:
    """Encode each sample as a fixed-width PCM binary codeword."""
    # Validate samples and quantization settings.
    quantize_samples(samples, bits_per_sample)

    levels = 2**bits_per_sample
    step_size = 2.0 / levels
    codewords = []

    for sample in samples:
        index = int((sample + 1.0) / step_size)
        index = min(index, levels - 1)

        codeword = format(index, f"0{bits_per_sample}b")
        codewords.append(codeword)

    return codewords

def decode_pcm(
    codewords: list[str],
    bits_per_sample: int = 8,
) -> list[float]:
    """Decode PCM binary codewords into reconstructed sample values."""
    if not codewords:
        raise ValueError("Codewords cannot be empty.")

    if not 1 <= bits_per_sample <= 16:
        raise ValueError("bits_per_sample must be between 1 and 16.")

    levels = 2**bits_per_sample
    step_size = 2.0 / levels
    decoded_samples = []

    for codeword in codewords:
        if not isinstance(codeword, str):
            raise ValueError("Each codeword must be a binary string.")

        if len(codeword) != bits_per_sample:
            raise ValueError(
                f"Each codeword must contain exactly {bits_per_sample} bits."
            )

        if any(bit not in "01" for bit in codeword):
            raise ValueError("Codewords must contain only 0 and 1.")

        index = int(codeword, 2)
        representative = -1.0 + (index + 0.5) * step_size
        decoded_samples.append(round(representative, 6))

    return decoded_samples
