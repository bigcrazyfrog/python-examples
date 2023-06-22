from integers_generator import integer


def test_output_numbers() -> None:
    """Test output numbers of generator."""
    int_generator = integer()
    for expected in range(1, 100):
        assert next(int_generator) == expected

    other_int_generator = integer()
    for expected in range(100, 120):
        assert next(other_int_generator) == expected
