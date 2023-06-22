import os
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import datetime, timedelta
from typing import Any

import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch
from requests import Session

GITHUB_URL_TEMPLATE = (
    "https://api.github.com/repos/{owner_login}/{repo_name}/commits"
)

GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


class GithubCommitsRepository:
    """Repository for Github API to interact with commits."""

    def _perform_paginated_requests(
        self,
        url: str,
        auth: tuple[str, str] | None = None,
        params: dict[str, str | int] | None = None,
    ) -> list[dict[str, dict[str, str]]]:
        """Get response from paginated requests.

        Perform paginated requests, combine data.

        Args:
            url: Response url path.
            auth: Authentication settings.
            params: Response parameters.

        Returns:
            Received json data.

        """
        if params is None:
            params = {}

        params["page"] = 1
        combined_json: list[dict[str, dict[str, str]]] = []

        with requests.Session() as session:
            session.auth = auth
            current_response_json: list[dict[str, dict[str, str]]] = []

            while len(current_response_json) != 0 or params["page"] == 1:
                response = session.get(url, params=params)
                response.raise_for_status()

                current_response_json = response.json()
                combined_json += current_response_json
                params["page"] += 1  # type: ignore

        return combined_json

    def get_committers(self, owner_login: str, repo_name: str) -> set[str]:
        """Get logins of unique users, who committed into repository.

        Args:
            owner_login: owner repository login.
            repo_name: Repository name.

        """
        url = GITHUB_URL_TEMPLATE .format(
            owner_login=owner_login,
            repo_name=repo_name,
        )
        auth = (GITHUB_CLIENT_ID, GITHUB_TOKEN)
        commits_data = self._perform_paginated_requests(url, auth)

        return set(
            commit["committer"]["login"]
            for commit in commits_data
        )

    def count_commits_last_month(
        self,
        owner_login: str,
        repo_name: str,
    ) -> int:
        """Count commits made last month.

        Args:
            owner_login: owner repository login.
            repo_name: Repository name.

        Returns:
            Number of last month commits.

        """
        since_date = datetime.today() - timedelta(days=30)
        params: dict[str, str | int] = {"since": str(since_date)}

        url = GITHUB_URL_TEMPLATE .format(
            owner_login=owner_login,
            repo_name=repo_name,
        )
        auth = (GITHUB_CLIENT_ID, GITHUB_TOKEN)
        commit_data = self._perform_paginated_requests(url, auth, params)

        return len(commit_data)

    def get_most_active_committer(
        self,
        owner_login: str,
        repo_name: str,
    ) -> str:
        """Get the most active committer of all time.

        Args:
            owner_login: owner repository login.
            repo_name: Repository name.

        """
        url = GITHUB_URL_TEMPLATE .format(
            owner_login=owner_login,
            repo_name=repo_name,
        )
        auth = (GITHUB_CLIENT_ID, GITHUB_TOKEN)
        commit_data = self._perform_paginated_requests(url, auth)

        committers = [
            commit["committer"]["login"]
            for commit in commit_data
        ]

        committers_counter = Counter(committers)
        return max(
            committers_counter,
            key=committers_counter.get,  # type: ignore
        )


# <------------------------------- Tests ----------------------------------->

@pytest.fixture
def github_repo() -> GithubCommitsRepository:
    """Fixture for GithubCommitRepository."""
    return GithubCommitsRepository()


class MockSessionResponse:
    """Session response mocker class."""

    def __init__(self, input_login_list: list[str]):
        self.json_data = self._prepare_committers_data(input_login_list)

    def _prepare_committers_data(
        self,
        login_list: list[str],
    ) -> Sequence[Mapping[str, dict[str, str]]]:
        """Parse string to json.

        Args:
            login_list: The list of user logins.

        Returns:
            Parsed data in json format.

        """
        return [{"committer": {"login": login}} for login in login_list]

    def json(self) -> Sequence[Mapping[str, dict[str, str]]]:
        """Get json from response."""
        return self.json_data

    def raise_for_status(self) -> None:
        """Raise for status.

        Raise if status is not OK.

        """


def mock_request_get(
    test_input: Any,
    **kwargs: dict[str, int],
) -> MockSessionResponse:
    """Get mock for get request function."""
    page: int = kwargs["params"]["page"]

    if page > len(test_input):
        return MockSessionResponse([])

    return MockSessionResponse(test_input[page - 1])


@pytest.mark.parametrize(
    ["committers", "expected"],
    [
        [
            [
                ["committer 1"],
            ],
            set(["committer 1"]),

        ],
        [
            [
                ["committer 1", "committer 1", "committer 2", "other"],
                ["second_page"],
            ],
            set(["committer 1", "committer 2", "other", "second_page"]),

        ],
        [
            [
                ["committer 0", "new login"],
                ["committer 0", "123"],
                ["login"],
            ],
            set(["committer 0", "new login", "123", "login"]),
        ],
    ],
)
def test_getting_committers(
    monkeypatch: MonkeyPatch,
    github_repo: GithubCommitsRepository,
    committers: list[list[str]],
    expected: set[str],
) -> None:
    """Test getting committers method."""
    monkeypatch.setattr(
        Session,
        "get",
        lambda *args, **kwargs: mock_request_get(committers, **kwargs),
    )

    committers_names = github_repo.get_committers("", "")
    assert committers_names == expected


@pytest.mark.parametrize(
    ["committers", "expected"],
    [
        [
            [
                ["committer 1"],
            ],
            1,
        ],
        [
            [
                ["committer 1", "committer 1", "committer 2", "other"],
                ["second_page"],
            ],
            5,

        ],
        [
            [
                ["committer 0", "new login"],
                ["committer 0", "123"],
                ["login"],
            ],
            5,
        ],
    ],
)
def test_count_commits_last_month(
    monkeypatch: MonkeyPatch,
    github_repo: GithubCommitsRepository,
    committers: list[list[str]],
    expected: int,
) -> None:
    """Test count commits from last month."""
    monkeypatch.setattr(
        Session,
        "get",
        lambda *args, **kwargs: mock_request_get(committers, **kwargs),
    )

    counter_commits = github_repo.count_commits_last_month("", "")
    assert counter_commits == expected


@pytest.mark.parametrize(
    ["committers", "expected"],
    [
        [
            [
                ["committer 1"],
            ],
            "committer 1",
        ],
        [
            [
                ["committer 1", "committer 1", "committer 2", "other"],
                ["second_page", "other", "other"],
                ["other"],
            ],
            "other",

        ],
        [
            [
                ["committer 0", "new login"],
                ["committer 0", "123"],
                ["login"],
            ],
            "committer 0",
        ],
    ],
)
def test_getting_most_active_committer(
    monkeypatch: MonkeyPatch,
    github_repo: GithubCommitsRepository,
    committers: list[list[str]],
    expected: str,
) -> None:
    """Test getting most active committer."""
    monkeypatch.setattr(
        Session,
        "get",
        lambda *args, **kwargs: mock_request_get(committers, **kwargs),
    )

    committers_names = github_repo.get_most_active_committer("", "")
    assert committers_names == expected
