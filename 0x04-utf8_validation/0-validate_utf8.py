#!/usr/bin/python3
"""
This is the `0-validate_utf` module. It contains the function `validUTF8`.
"""
from typing import List


def validUTF8(data: List[int]) -> bool:
    """
    validUTF8 validates if the data is valid UTF-8.
    A character in UTF-8 can be 1 to 4 bytes long.
    The data set can contain multiple characters.
    The data will be represented by a list of integers.
    Each integer represents 1 byte of data, therefore it only handles the 8
    least significant bits of each integer.
    Return: True if data is a valid UTF-8 encoding, else return False.
    """
    if type(data) != list or not all(isinstance(i, int) for i in data):
        print("data must be a list of integers")
        return False

    num_bytes = 0

    for num in data:
        # Check if the current data is the start of a new character.
        if num_bytes == 0:
            mask = 1 << 7
            while mask & num:
                num_bytes += 1
                mask >>= 1

            # Validate number of bytes for the character.
            if num_bytes == 0:
                # It's a single byte character, hence num_bytes remains zero.
                continue
            elif num_bytes == 1 or num_bytes > 4:
                return False
        else:
            # Check if the current byte is a continuation byte of a character.
            if not (num & (1 << 7) and not (num & (1 << 6))):
                return False

        # Decrement the number of bytes left to process for the character.
        num_bytes -= 1

    return num_bytes == 0


if __name__ == "__main__":
    data = [65]
    print(validUTF8(data))  # Output True

    data = [80, 121, 116, 104, 111, 110, 32,
            105, 115, 32, 99, 111, 111, 108, 33]
    print(validUTF8(data))  # Output True

    data = [229, 65, 127, 256]
    print(validUTF8(data))  # Output False
