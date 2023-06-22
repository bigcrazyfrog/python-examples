from connectator import chain_generator


def test_chain_generator() -> None:
    """Test chain generator."""
    data_list = [1, 2, "str", 3.4]
    data_tuple = (3, "a", int)
    data_iter = iter(data_list)
    data_range = range(5)

    result = chain_generator(data_list, data_tuple, data_iter, data_range)
    expected = data_list + list(data_tuple) + data_list + list(data_range)

    assert list(result) == expected
