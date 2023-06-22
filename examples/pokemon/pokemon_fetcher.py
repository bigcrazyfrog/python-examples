from collections.abc import Generator
from typing import Any

import requests


def get_json_from_response(
    url: str,
    session: requests.Session,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Get JSON data from response.

    Raises:
        HTTPError: Base error in HTTP response.

    """
    response = session.get(url, params=params)
    response.raise_for_status()

    return response.json()


def pokemon_fetcher(
    url: str,
    limit: int = 100,
    offset: int = 0,
) -> Generator[dict[str, Any], None, None]:
    """Get response from paginated requests.

    Perform paginated requests, combine data.

    """
    url += f"?offset={offset}&limit={limit}"

    with requests.Session() as session:
        while url:
            current_response_json = get_json_from_response(url, session)
            yield from current_response_json["results"]

            url = current_response_json["next"]
