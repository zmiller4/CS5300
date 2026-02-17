from __future__ import annotations

import httpx
import pytest

from task7 import RepoInfo, fetch_repo_info, parse_github_repo_url


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://github.com/zmiller4/CS5300", ("zmiller4", "CS5300")),
        ("https://github.com/zmiller4/CS5300/", ("zmiller4", "CS5300")),
        ("https://github.com/zmiller4/CS5300.git", ("zmiller4", "CS5300")),
        ("https://github.com/zmiller4/CS5300#readme", ("zmiller4", "CS5300")),
    ],
)
def test_parse_github_repo_url(url, expected):
    assert parse_github_repo_url(url) == expected


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/zmiller4/CS5300",
        "https://github.com/onlyowner",
        "not a url",
    ],
)
def test_parse_github_repo_url_invalid(url):
    with pytest.raises(ValueError):
        parse_github_repo_url(url)


def test_fetch_repo_info_success():
    payload = {
        "name": "CS5300",
        "full_name": "zmiller4/CS5300",
        "html_url": "https://github.com/zmiller4/CS5300",
        "stargazers_count": 7,
        "forks_count": 2,
        "open_issues_count": 1,
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == httpx.URL("https://api.github.com/repos/zmiller4/CS5300")
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    info = fetch_repo_info("https://github.com/zmiller4/CS5300", client=client)
    assert info == RepoInfo(
        name="CS5300",
        full_name="zmiller4/CS5300",
        html_url="https://github.com/zmiller4/CS5300",
        stargazers_count=7,
        forks_count=2,
        open_issues_count=1,
    )

    client.close()


def test_fetch_repo_info_http_error():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "Not Found"})

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    with pytest.raises(httpx.HTTPStatusError):
        fetch_repo_info("https://github.com/zmiller4/CS5300", client=client)

    client.close()
