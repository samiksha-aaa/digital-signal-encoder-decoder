
import numpy as np
import matplotlib.pyplot as plt



def plot_line_code(
    bits: str,
    signal: list[int],
    scheme: str,
    samples_per_bit: int = 100,
) -> None:
    """Plot line codes with one or multiple levels per bit."""
    if not bits:
        raise ValueError("Bitstream cannot be empty.")

    if len(bits) != len(signal) and len(signal) % len(bits) != 0:
        raise ValueError("Signal length must be a multiple of bit length.")

    if any(level not in (-1, 1) for level in signal):
        raise ValueError("Signal levels must be -1 or +1.")

    if samples_per_bit < 1:
        raise ValueError("Samples per bit must be positive.")

    levels_per_bit = len(signal) // len(bits)
    samples_per_level = samples_per_bit // levels_per_bit

    if samples_per_bit % levels_per_bit != 0:
        raise ValueError(
            "Samples per bit must be divisible by levels per bit."
        )

    levels = np.repeat(signal, samples_per_level)
    time = np.arange(len(levels)) / samples_per_bit

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.step(time, levels, where="post", linewidth=2)

    # Draw boundaries at each encoded level.
    for boundary in range(len(signal) + 1):
        x = boundary / levels_per_bit
        ax.axvline(x, color="gray", alpha=0.25, linewidth=0.8)

    # Original data bits appear at the center of each bit interval.
    for index, bit in enumerate(bits):
        ax.text(
            index + 0.5,
            1.35,
            bit,
            ha="center",
            va="center",
            fontsize=11,
        )

    ax.set_title(f"{scheme} Line Coding")
    ax.set_xlabel("Time (bit intervals)")
    ax.set_ylabel("Signal level")
    ax.set_xlim(0, len(bits))
    ax.set_ylim(-1.6, 1.7)
    ax.set_yticks([-1, 0, 1])
    ax.set_xticks(range(len(bits) + 1))
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    plt.show()

