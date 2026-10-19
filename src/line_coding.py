from .scrambling import encode_ami
def _validate_bits(bits: str) -> None:
    """Ensure the input contains only binary digits."""
    if not bits:
        raise ValueError("Bitstream cannot be empty.")

    if any(bit not in "01" for bit in bits):
        raise ValueError("Bitstream must contain only 0s and 1s.")


def encode_nrz_l(bits: str) -> list[int]:
    """NRZ-L: 1 -> +1, 0 -> -1."""
    _validate_bits(bits)

    return [1 if bit == "1" else -1 for bit in bits]


def encode_nrz_i(bits: str, initial_level: int = -1) -> list[int]:
    """
    NRZ-I: a 1 causes a transition; a 0 keeps the current level.
    The initial signal level defaults to -1.
    """
    _validate_bits(bits)

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be -1 or +1.")

    level = initial_level
    signal = []

    for bit in bits:
        if bit == "1":
            level *= -1

        signal.append(level)

    return signal


def encode_manchester(bits: str) -> list[int]:
    """Manchester: 0 -> high-low, 1 -> low-high."""
    _validate_bits(bits)

    signal = []

    for bit in bits:
        if bit == "0":
            signal.extend([1, -1])
        else:
            signal.extend([-1, 1])

    return signal


def encode_differential_manchester(
    bits: str,
    initial_level: int = 1,
) -> list[int]:
    """
    Differential Manchester:
    0 -> transition at the beginning.
    1 -> no transition at the beginning.
    Every bit has a midpoint transition.
    """
    _validate_bits(bits)

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be -1 or +1.")

    level = initial_level
    signal = []

    for bit in bits:
        if bit == "0":
            level *= -1

        # First half of the bit.
        signal.append(level)

        # Mandatory midpoint transition.
        level *= -1
        signal.append(level)

    return signal

# Registry: add future line-coding schemes here.
LINE_ENCODERS = {
    "NRZ-L": encode_nrz_l,
    "NRZ-I": encode_nrz_i,
    "Manchester": encode_manchester,
    "Differential Manchester": encode_differential_manchester,
      "AMI": encode_ami,
}



def encode(bits: str, scheme: str) -> list[int]:
    """Encode a bitstream using the selected scheme."""
    try:
        encoder = LINE_ENCODERS[scheme]
    except KeyError:
        raise ValueError(f"Unsupported line-coding scheme: {scheme}") from None

    return encoder(bits)
