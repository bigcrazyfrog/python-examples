from enum import StrEnum

import pytest
from _pytest.monkeypatch import MonkeyPatch

MIN_ALLOWED_NUMBER = 1
MAX_ALLOWED_NUMBER = 8


class CubeCollectionState(StrEnum):
    """Contains enums for watching recommendations."""
    WRONG_INPUT = "Incorrect input!"
    END = "The cube was assembled."


def check_number_in_allowed_range(
    input_number: str,
    min_allowed_number: int,
    max_allowed_number: int,
) -> bool:
    """Check is number in allowed range.

    Args:
        input_number: String with number to check.

    Returns:
        True if the number is correct, False otherwise.

    """
    if not input_number.isdigit():
        return False

    number = int(input_number)
    return min_allowed_number <= number <= max_allowed_number


def collect_cube() -> None:
    """Collect cube by number from 1 to 6.

    Consistently get numbers from 1-8 from a user as an input, until the
    function will collect 1-2-3-4-5-6 numbers.

    """
    collected_numbers: set[int] = set()

    while len(collected_numbers) != 6:
        input_number = input()

        if not check_number_in_allowed_range(
            input_number,
            MIN_ALLOWED_NUMBER,
            MAX_ALLOWED_NUMBER,
        ):
            print(CubeCollectionState.WRONG_INPUT.value)
            continue

        number = int(input_number)
        if number <= 6:
            collected_numbers.add(number)

    print(CubeCollectionState.END.value)


if __name__ == "__main__":
    collect_cube()


# <------------------------------- Tests ----------------------------------->

class UserManager:
    """Manager for collecting input and output data."""

    def __init__(self, user_input: str):
        self.input_queue = user_input.split()
        self.output_cache: list[str] = []
        self.index = 0

    def input(self) -> str:
        """Returned next input message."""
        value = self.input_queue[self.index]
        self.index += 1
        return value

    def output(self, output_message: str) -> None:
        """Register output string."""
        self.output_cache.append(output_message)


@pytest.mark.parametrize(
    ["test_input", "printed_messages"],
    [
        [
            "1 2 3 4 5 6", [CubeCollectionState.END],
        ],
        [
            "1 1 2 2 6 4 5 1 2 6 3", [CubeCollectionState.END],
        ],
        [
            "7 8 2 8 2 2 2 1 2 3 4 5 6", [CubeCollectionState.END],
        ],
        [
            "9 7 8 2 8 2 0 2 2 10000 1 2 3 4 5 wrong 6",
            [
                CubeCollectionState.WRONG_INPUT,
                CubeCollectionState.WRONG_INPUT,
                CubeCollectionState.WRONG_INPUT,
                CubeCollectionState.WRONG_INPUT,
                CubeCollectionState.END,
            ],
        ],
    ],
)
def test_collecting_cube(
    monkeypatch: MonkeyPatch,
    test_input: str,
    printed_messages: list[CubeCollectionState],
) -> None:
    """Test cube collecting."""
    user_manager = UserManager(test_input)

    monkeypatch.setattr("builtins.input", user_manager.input)
    monkeypatch.setattr("builtins.print", user_manager.output)

    collect_cube()

    assert user_manager.index == len(user_manager.input_queue)
    assert user_manager.output_cache == printed_messages
