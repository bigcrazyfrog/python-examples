from collections import Counter

import pytest


def can_be_palindrome(input_string: str) -> bool:
    """Check if the input string can be a palindrome.

    We can create palindrome if we have less than two odd entry of symbol.

    Args:
        input_string: String to check.

    Returns:
        True for if a palindrome could be created, False otherwise.

    """
    char_counter = Counter(input_string)

    odd_char_entries_count = sum(count % 2 for count in char_counter.values())

    return odd_char_entries_count < 2


# <------------------------------- Tests ----------------------------------->

@pytest.mark.parametrize(
    "test_input",
    ["abcdcba", "aabbcc", "", "125141154", "a"],
)
def test_string_can_be_palindrome(test_input: str) -> None:
    """Test string can be a palindrome."""
    assert can_be_palindrome(test_input)


def test_string_cannot_be_palindrome() -> None:
    """Test string can't be a palindrome."""
    assert not can_be_palindrome("abcde")
