
from .data_generator import (
    generate_random_bits,
    generate_bits_with_zeros,
    longest_palindrome,
)
from .line_coding import LINE_ENCODERS, encode
from .plotting import plot_line_code


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

        for index, scheme in enumerate(schemes, start=1):
            print(f"{index}. {scheme}")

        scheme_choice = int(input("Choose a line-coding scheme: "))

        if not 1 <= scheme_choice <= len(schemes):
            print("Invalid line-coding option.")
            return

        scheme = schemes[scheme_choice - 1]
        signal = encode(bits, scheme)

        print("\nSelected scheme:", scheme)
        print("Encoded signal levels:", signal)

        plot_line_code(bits, signal, scheme)

    except ValueError as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
