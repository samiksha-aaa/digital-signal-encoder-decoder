
import numpy as np
import matplotlib.pyplot as plt


def plot_line_code(
    bits: str,
    signal: list[int],
    scheme: str,
    samples_per_bit: int = 100,
) -> None:
    """Plot an encoded digital waveform."""
    if len(bits) != len(signal):
        raise ValueError("Bits and encoded signal must have equal lengths.")

    if samples_per_bit < 1:
        raise ValueError("Samples per bit must be positive.")

    levels = np.repeat(signal, samples_per_bit)
    time = np.arange(len(levels)) / samples_per_bit

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.step(time, levels, where="post", linewidth=2)

    # Mark the boundaries between consecutive bits.
    for boundary in range(len(bits) + 1):
        ax.axvline(boundary, color="gray", alpha=0.25, linewidth=0.8)

    # Display the original bit above each bit interval.
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
