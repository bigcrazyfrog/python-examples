from collections.abc import Iterator


class IntegerGenerator(Iterator[int]):
    """State-aware integers generator.

    Generate sequences of integer numbers from 1 to infinity.

    """
    _counter: int = 0

    @classmethod
    def __next__(cls) -> int:
        cls._counter += 1
        return cls._counter

    def __iter__(self) -> Iterator[int]:
        return self


def integer() -> Iterator[int]:
    """State-aware integers generator."""
    return IntegerGenerator()
