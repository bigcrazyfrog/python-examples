import time
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeAlias, TypeVar

RT = TypeVar("RT")  # Function return values
P = ParamSpec("P")  # Function parameters

FuncType: TypeAlias = Callable[[Callable[P, RT]], Callable[P, RT]]

MILLISECONDS_PER_SECOND = 1000


def backoff(
    exceptions: tuple[type[BaseException], ...],
    max_retry_count: int | None = 3,
    delay: int = 0,
) -> FuncType[P, RT]:
    """Retry function calls if it raises exceptions.

    Args:
        exceptions: Exceptions to do retiring on.
        max_retry_count: Count of maximum attempts of retrying.
        delay: Delay in milliseconds between retry attempts.

    """
    def _decorate(func: Callable[P, RT]) -> Callable[P, RT]:
        @wraps(func)
        def _wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
            count = max_retry_count
            while True:
                if count is not None:
                    count -= 1
                # Mustn't ignore exception on last iteration.
                if count == 0:
                    return func(*args, **kwargs)
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    time.sleep(delay / MILLISECONDS_PER_SECOND)
        return _wrapper
    return _decorate
