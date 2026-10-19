
import random


def generate_random_bits(length: int) -> str:
    """Generate a completely random binary sequence."""
    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    return "".join(random.choices("01", k=length))


def generate_bits_with_zeros(length: int, zero_count: int) -> str:
    """Generate random bits containing a guaranteed run of zeros."""
    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    if zero_count not in (4, 8):
        raise ValueError("Zero count must be either 4 or 8.")

    if zero_count > length:
        raise ValueError("Length must be at least the zero count.")

    bits = list(generate_random_bits(length))

    # Choose a valid starting position for the zero sequence.
    start = random.randint(0, length - zero_count)
    bits[start:start + zero_count] = ["0"] * zero_count

    return "".join(bits)


def longest_palindrome(bits: str) -> str:
    """
    Find the longest palindromic substring using Manacher's algorithm.
    Time complexity: O(n).
    Space complexity: O(n).
    """
    if not bits:
        return ""

    # Transform: 101 -> ^#1#0#1#$
    transformed = "^#" + "#".join(bits) + "#$"
    radius = [0] * len(transformed)

    center = 0
    right = 0

    for i in range(1, len(transformed) - 1):
        mirror = 2 * center - i

        if i < right:
            radius[i] = min(right - i, radius[mirror])

        # Expand around the current center.
        while transformed[i + 1 + radius[i]] == transformed[i - 1 - radius[i]]:
            radius[i] += 1

        # Update the rightmost palindrome.
        if i + radius[i] > right:
            center = i
            right = i + radius[i]

    # Find the center with the largest palindrome.
    best_center = max(range(len(radius)), key=radius.__getitem__)
    best_length = radius[best_center]

    # Map transformed-string coordinates back to original bits.
    start = (best_center - best_length) // 2
    return bits[start:start + best_length]
