
from .data_generator import (
    generate_random_bits,
    generate_bits_with_zeros,
    longest_palindrome,
)
from .line_coding import LINE_ENCODERS, encode
from .plotting import plot_line_code
from .scrambling import encode_ami, encode_b8zs, encode_hdb3


def main():
    print("\n=== Digital Signal Encoder and Decoder ===")
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
