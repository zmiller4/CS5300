"""
Task 7: Package Management
GitHub REST API using httpx
"""

from __future__ import annotations
from dataclasses import dataclass
import httpx

@dataclass(frozen=True)
class RepoInfo:
    name: str
    full_name: str
    html_url: str
    stargazers_count: int
    forks_count: int
    open_issues_count: int

OWNER = "zmiller4"
REPO = "CS5300"

def fetch_repo_info(client: httpx.Client | None = None) -> RepoInfo:
    api_url = f"https://api.github.com/repos/{OWNER}/{REPO}"

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

def main() -> None:
    info = fetch_repo_info()
    print(info)


if __name__ == "__main__":
    main()
