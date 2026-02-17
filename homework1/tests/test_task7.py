from __future__ import annotations

import httpx
import pytest

from task7 import OWNER, REPO, RepoInfo, fetch_repo_info


def test_fetch_repo_info_success():
    payload = {
        "name": "CS5300",
        "full_name": f"{OWNER}/{REPO}",
        "html_url": f"https://github.com/{OWNER}/{REPO}",
        "stargazers_count": 7,
        "forks_count": 2,
        "open_issues_count": 1,
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == httpx.URL(f"https://api.github.com/repos/{OWNER}/{REPO}")
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    info = fetch_repo_info(client=client)
    assert info == RepoInfo(
        name="CS5300",
        full_name=f"{OWNER}/{REPO}",
        html_url=f"https://github.com/{OWNER}/{REPO}",
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
        fetch_repo_info(client=client)

    client.close()
