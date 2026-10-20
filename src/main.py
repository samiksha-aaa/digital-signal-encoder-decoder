
from .data_generator import (
    generate_random_bits,
    generate_bits_with_zeros,
    longest_palindrome,
)
from .line_coding import LINE_ENCODERS, encode
from .plotting import plot_line_code
from .scrambling import encode_ami, encode_b8zs, encode_hdb3
from .decoder import (
    decode_nrz_l,
    decode_nrz_i,
    decode_manchester,
    decode_differential_manchester,
    decode_ami,
    decode_b8zs,
    decode_hdb3,
)
from .pcm import quantize_samples, encode_pcm, decode_pcm


def decode_signal_menu():
    print("\n--- Signal Decoding ---")
    print("1. NRZ-L")
    print("2. NRZ-I")
    print("3. Manchester")
    print("4. Differential Manchester")
    print("5. AMI")
    print("6. B8ZS")
    print("7. HDB3")

    options = {
        "1": ("NRZ-L", decode_nrz_l),
        "2": ("NRZ-I", decode_nrz_i),
        "3": ("Manchester", decode_manchester),
        "4": ("Differential Manchester", decode_differential_manchester),
        "5": ("AMI", decode_ami),
        "6": ("B8ZS", decode_b8zs),
        "7": ("HDB3", decode_hdb3),
    }

    choice = input("Choose a decoding scheme (1-7): ").strip()

    if choice not in options:
        print("Invalid decoding option.")
        return

    scheme, decoder = options[choice]

    try:
        raw_signal = input(
            "Enter comma-separated signal levels "
            "(e.g. 1,0,-1,1): "
        )
        signal = [int(value.strip()) for value in raw_signal.split(",")]

        decoded_bits = decoder(signal)

        print("\nSelected decoder:", scheme)
        print("Decoded binary data:", decoded_bits)

    except ValueError as error:
        print("Decoding error:", error)


def pcm_menu():
    print("\n--- PCM Encoding and Decoding ---")
    print("Enter sample amplitudes between -1.0 and 1.0.")
    print("Example: -1.0, -0.5, 0.0, 0.5, 1.0")

    try:
        raw_samples = input("Enter sample amplitudes: ")
        samples = [
            float(value.strip())
            for value in raw_samples.split(",")
        ]

        bits_per_sample = int(
            input("Enter bits per sample (1-16): ")
        )

        quantized = quantize_samples(samples, bits_per_sample)
        codewords = encode_pcm(samples, bits_per_sample)
        reconstructed = decode_pcm(codewords, bits_per_sample)

        print("\nOriginal samples:", samples)
        print("Quantized samples:", quantized)
        print("PCM binary codewords:", codewords)
        print("Reconstructed samples:", reconstructed)

    except ValueError as error:
        print("PCM input error:", error)


def main():
    print("\n=== Digital Signal Encoder and Decoder ===")
    print("1. Generate data, encode, and plot")
    print("2. Decode an existing signal")
    print("3. PCM encode and decode")

    main_choice = input("Choose an option (1/2/3): ").strip()

    if main_choice == "2":
        decode_signal_menu()
        return

    if main_choice == "3":
        pcm_menu()
        return

    if main_choice != "1":
        print("Invalid main-menu option.")
        return

    print("\n--- Digital Data Generation ---")
    print("1. Completely random binary data")
    print("2. Binary data with consecutive zeros")

    try:
        choice = input("Choose an option (1/2): ").strip()
        length = int(input("Enter the sequence length: "))

        if choice == "1":
            bits = generate_random_bits(length)

        elif choice == "2":
            zero_count = int(
                input("Choose consecutive zeros (4 or 8): ")
            )
            bits = generate_bits_with_zeros(length, zero_count)

        else:
            print("Invalid data-generation option.")
            return

        print("\nGenerated digital data:", bits)
        print("Longest palindrome:", longest_palindrome(bits))

        print("\n--- Line Coding ---")
        schemes = list(LINE_ENCODERS.keys())

        for index, item in enumerate(schemes, start=1):
            print(f"{index}. {item}")

        scheme_choice = int(input("Choose a line-coding scheme: "))

        if not 1 <= scheme_choice <= len(schemes):
            print("Invalid line-coding option.")
            return

        scheme = schemes[scheme_choice - 1]

        if scheme != "AMI":
            signal = encode(bits, scheme)

        else:
            scramble_choice = input(
                "Apply scrambling? (y/n): "
            ).strip().lower()

            if scramble_choice == "n":
                signal = encode_ami(bits)

            elif scramble_choice == "y":
                scrambling_options = {
                    "1": ("B8ZS", encode_b8zs),
                    "2": ("HDB3", encode_hdb3),
                }

                print("1. B8ZS")
                print("2. HDB3")

                scramble_type = input(
                    "Choose scrambling type: "
                ).strip()

                if scramble_type not in scrambling_options:
                    print("Invalid scrambling option.")
                    return

                scramble_name, scramble_function = (
                    scrambling_options[scramble_type]
                )

                signal = scramble_function(bits)
                scheme = f"AMI + {scramble_name}"

            else:
                print("Please enter y or n.")
                return

        print("\nSelected scheme:", scheme)
        print("Encoded signal levels:", signal)

        plot_line_code(bits, signal, scheme)

    except ValueError as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
