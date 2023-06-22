from collections.abc import Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")


def chain_generator(*iterables: Iterable[T]) -> Iterator[T]:
    """Connect iterable objects.

    Generator function which concatenates together several iterable objects.

    Returns:
        An iterator through all their elements.

    """
    for iterable_obj in iterables:
        yield from iterable_obj
