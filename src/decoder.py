
def decode_nrz_l(signal: list[int]) -> str:
    """Decode an NRZ-L signal into binary data."""
    if not signal:
        raise ValueError("Signal cannot be empty.")

    if any(level not in (-1, 1) for level in signal):
        raise ValueError("NRZ-L levels must be -1 or +1.")

    return "".join("1" if level == 1 else "0" for level in signal)


def decode_nrz_i(signal: list[int], initial_level: int = -1) -> str:
    """Decode NRZ-I using the same initial level as the encoder."""
    if not signal:
        raise ValueError("Signal cannot be empty.")

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be -1 or +1.")

    if any(level not in (-1, 1) for level in signal):
        raise ValueError("NRZ-I levels must be -1 or +1.")

    bits = []
    previous_level = initial_level

    for level in signal:
        if level != previous_level:
            bits.append("1")
        else:
            bits.append("0")

        previous_level = level

    return "".join(bits)


def decode_manchester(signal: list[int]) -> str:
    """Decode Manchester signal using the project's encoding convention."""
    if not signal:
        raise ValueError("Signal cannot be empty.")

    if len(signal) % 2 != 0:
        raise ValueError("Manchester signal length must be even.")

    if any(level not in (-1, 1) for level in signal):
        raise ValueError("Manchester levels must be -1 or +1.")

    bits = []

    for i in range(0, len(signal), 2):
        pair = signal[i:i + 2]

        if pair == [1, -1]:
            bits.append("0")
        elif pair == [-1, 1]:
            bits.append("1")
        else:
            raise ValueError("Invalid Manchester signal pair.")

    return "".join(bits)


def decode_differential_manchester(
    signal: list[int],
    initial_level: int = 1,
) -> str:
    """Decode Differential Manchester using the project's encoding convention."""
    if not signal:
        raise ValueError("Signal cannot be empty.")

    if len(signal) % 2 != 0:
        raise ValueError("Differential Manchester signal length must be even.")

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be -1 or +1.")

    if any(level not in (-1, 1) for level in signal):
        raise ValueError("Signal levels must be -1 or +1.")

    bits = []
    previous_level = initial_level

    for i in range(0, len(signal), 2):
        first_half = signal[i]
        second_half = signal[i + 1]

        if first_half == second_half:
            raise ValueError("Invalid Differential Manchester pair.")

        # A transition at the start of a bit means 0.
        if first_half != previous_level:
            bits.append("0")
        else:
            bits.append("1")

        previous_level = second_half

    return "".join(bits)

def decode_ami(signal: list[int]) -> str:
    """Decode an AMI signal into binary data."""
    if not signal:
        raise ValueError("Signal cannot be empty.")

    if any(level not in (-1, 0, 1) for level in signal):
        raise ValueError("AMI levels must be -1, 0, or +1.")

    # In AMI, zero represents bit 0 and either pulse polarity represents bit 1.
    return "".join("0" if level == 0 else "1" for level in signal)

def decode_b8zs(signal: list[int]) -> str:
    """Decode a B8ZS signal by replacing standard violation patterns with zeros."""
    if not signal:
        raise ValueError("Signal cannot be empty.")

    if any(level not in (-1, 0, 1) for level in signal):
        raise ValueError("Signal levels must be -1, 0, or +1.")

    bits = []
    i = 0
    last_pulse = -1

    while i < len(signal):
        # B8ZS pattern after a positive previous pulse:
        # 000+-0-+
        if signal[i:i + 8] == [0, 0, 0, 1, -1, 0, -1, 1] and last_pulse == 1:
            bits.extend("00000000")
            last_pulse = 1
            i += 8

        # B8ZS pattern after a negative previous pulse:
        # 000-+0+-
        elif signal[i:i + 8] == [0, 0, 0, -1, 1, 0, 1, -1] and last_pulse == -1:
            bits.extend("00000000")
            last_pulse = -1
            i += 8

        else:
            level = signal[i]

            if level == 0:
                bits.append("0")
            else:
                bits.append("1")
                last_pulse = level

            i += 1

    return "".join(bits)


def decode_hdb3(signal: list[int]) -> str:
    """Decode HDB3 by recognizing 000V and B00V substitution patterns."""
    if not signal:
        raise ValueError("Signal cannot be empty.")

    if any(level not in (-1, 0, 1) for level in signal):
        raise ValueError("Signal levels must be -1, 0, or +1.")

    bits = []
    i = 0
    last_pulse = -1
    pulses_since_violation = 0

    while i < len(signal):
        # B00V: B has polarity opposite to the previous pulse;
        # V has the same polarity as B.
        if (
            i + 3 < len(signal)
            and signal[i] == -last_pulse
            and signal[i + 1] == 0
            and signal[i + 2] == 0
            and signal[i + 3] == signal[i]
        ):
            bits.extend("0000")
            last_pulse = signal[i + 3]
            pulses_since_violation = 0
            i += 4

        # 000V: V repeats the polarity of the previous pulse.
        elif (
            i + 3 < len(signal)
            and signal[i] == 0
            and signal[i + 1] == 0
            and signal[i + 2] == 0
            and signal[i + 3] == last_pulse
            and pulses_since_violation % 2 == 1
        ):
            bits.extend("0000")
            last_pulse = signal[i + 3]
            pulses_since_violation = 0
            i += 4

        else:
            level = signal[i]

            if level == 0:
                bits.append("0")
            else:
                bits.append("1")
                last_pulse = level
                pulses_since_violation += 1

            i += 1

    return "".join(bits)
