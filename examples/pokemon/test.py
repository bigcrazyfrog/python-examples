from itertools import chain

import requests
from pokemon_fetcher import get_json_from_response, pokemon_fetcher


def test_get_json_from_response(requests_mock):
    """Test getting JSON data from response."""
    url = "mock://test.com"
    expected_json = {"a": 1, "info": {"name": "John", "salary": 100}}

    requests_mock.get(url, json=expected_json)

    with requests.Session() as session:
        json_data = get_json_from_response(url, session)

        assert json_data == expected_json


def test_pokemon_fetcher(requests_mock):
    """Test get JSON data by api fetcher."""
    url = "mock://test.com/{}"
    input_names = [
        ["no name"],
        ["bulbasaur", "ivysaur", "venusaur"],
        ["John", "Sanya"],
        ["Name", "Other name"],
    ]

    for index, names in enumerate(input_names):
        next_url = url.format(index + 1)
        expected_json = {
            "next": next_url if index + 1 < len(input_names) else None,
            "results": [{"name": name} for name in names],
        }
        requests_mock.get(url.format(index), json=expected_json)

    name_list = chain(*input_names)
    for result in pokemon_fetcher(url.format(0)):
        assert result["name"] == next(name_list)
