"""
Task 7: Package Management
GitHub REST API using httpx
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

import httpx


@dataclass(frozen=True)
class RepoInfo:
    name: str
    full_name: str
    html_url: str
    stargazers_count: int
    forks_count: int
    open_issues_count: int


def parse_github_repo_url(url: str) -> tuple[str, str]:
    p = urlparse(url)
    if p.netloc not in {"github.com", "www.github.com"}:
        raise ValueError("Not a github.com URL")

    parts = [x for x in p.path.split("/") if x]
    if len(parts) < 2:
        raise ValueError("Repo URL must look like /owner/repo")

    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo


def fetch_repo_info(url: str, client: httpx.Client | None = None) -> RepoInfo:
    owner, repo = parse_github_repo_url(url)
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    c = client or httpx.Client(timeout=10.0, headers={"User-Agent": "cs5300-task7"})
    try:
        r = c.get(api_url, headers={"Accept": "application/vnd.github+json"})
        r.raise_for_status()
        data = r.json()
    finally:
        if client is None:
            c.close()

    return RepoInfo(
        name=str(data["name"]),
        full_name=str(data["full_name"]),
        html_url=str(data["html_url"]),
        stargazers_count=int(data["stargazers_count"]),
        forks_count=int(data["forks_count"]),
        open_issues_count=int(data["open_issues_count"]),
    )


if __name__ == "__main__":
    info = fetch_repo_info("https://github.com/zmiller4/CS5300")
    print(info)
