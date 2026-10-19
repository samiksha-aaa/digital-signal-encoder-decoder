
def _validate_bits(bits: str) -> None:
    if not bits:
        raise ValueError("Bitstream cannot be empty.")

    if any(bit not in "01" for bit in bits):
        raise ValueError("Bitstream must contain only 0s and 1s.")


def encode_ami(bits: str) -> list[int]:
    """AMI: zeros map to 0; ones alternate between +1 and -1."""
    _validate_bits(bits)

    signal = []
    last_pulse = -1

    for bit in bits:
        if bit == "1":
            last_pulse *= -1
            signal.append(last_pulse)
        else:
            signal.append(0)

    return signal


def encode_b8zs(bits: str) -> list[int]:
    """
    B8ZS scrambling.
    Replace each run of eight zeros with 000VB0VB.
    """
    _validate_bits(bits)

    signal = []
    last_pulse = -1
    i = 0

    while i < len(bits):
        if bits[i] == "1":
            last_pulse *= -1
            signal.append(last_pulse)
            i += 1
            continue

        # Check whether eight zeros begin at this position.
        if bits[i:i + 8] == "00000000":
            # Pattern depends on the preceding pulse polarity.
            if last_pulse == 1:
                pattern = [0, 0, 0, 1, -1, 0, -1, 1]
            else:
                pattern = [0, 0, 0, -1, 1, 0, 1, -1]

            signal.extend(pattern)
            last_pulse = pattern[-1]
            i += 8
        else:
            signal.append(0)
            i += 1

    return signal


def encode_hdb3(bits: str) -> list[int]:
    """
    HDB3 scrambling.
    Replace four zeros with 000V or B00V.
    """
    _validate_bits(bits)

    signal = []
    last_pulse = -1
    pulses_since_violation = 0
    i = 0

    while i < len(bits):
        if bits[i] == "1":
            last_pulse *= -1
            signal.append(last_pulse)
            pulses_since_violation += 1
            i += 1
            continue

        if bits[i:i + 4] == "0000":
            if pulses_since_violation % 2 == 1:
                # 000V: V has the same polarity as the previous pulse.
                violation = last_pulse
                signal.extend([0, 0, 0, violation])
                last_pulse = violation
            else:
                # B00V: B is a normal pulse; V repeats B's polarity.
                balancing = -last_pulse
                violation = balancing
                signal.extend([balancing, 0, 0, violation])
                last_pulse = violation

            pulses_since_violation = 0
            i += 4
        else:
            signal.append(0)
            i += 1

    return signal
