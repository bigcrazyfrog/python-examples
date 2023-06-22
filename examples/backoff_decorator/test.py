from collections.abc import Iterable

import pytest
from backoff import backoff


@backoff(exceptions=(ValueError, IndentationError, IndexError))
def func_without_error():
    """Function without error."""
    return "Successful"


@backoff(exceptions=(ZeroDivisionError), max_retry_count=3)
def division(number_iterator: Iterable[int]) -> int:
    """Get division by number.

    Raises:
        ZeroDivisionError: Raise if input number is zero.

    """
    return 6 / next(number_iterator)


def test_no_error_func():
    """Test function without error."""
    assert func_without_error() == "Successful"


def test_backoff():
    """Test backoff function with three tries of call.

    First two call raise error, third call successful.

    """
    number_iterator = iter([0, 0, 2])

    assert division(number_iterator) == 3


def test_backoff_max_retry_count():
    """Test raise error after `max_retry_count`."""
    number_iterator = iter([0, 0, 0, 2])

    with pytest.raises(ZeroDivisionError):
        division(number_iterator)
