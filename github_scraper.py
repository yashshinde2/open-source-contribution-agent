import os
import requests
from typing import List, Dict, Any, Optional

try:
    from github import Github, Auth
    PYGITHUB_AVAILABLE = True
except ImportError:
    PYGITHUB_AVAILABLE = False

from config_loader import AppConfig

class GitHubScraper:
    """Scrapes fresh good first issues from GitHub API."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self._github = None
        if PYGITHUB_AVAILABLE and self.token:
            auth = Auth.Token(self.token)
            self._github = Github(auth=auth)

    def fetch_issues(self, config: AppConfig) -> List[Dict[str, Any]]:
        """Fetch fresh issues from target repos or global GitHub search."""
        issues_data = []
        seen_ids = set()

        if config.target_repos:
            for repo_name in config.target_repos:
                try:
                    repo_issues = self._fetch_repo_issues(repo_name, labels=config.search_labels, limit=5)
                    for issue in repo_issues:
                        if issue["id"] not in seen_ids:
                            seen_ids.add(issue["id"])
                            issues_data.append(issue)
                except Exception as e:
                    print(f"Error fetching issues for repo {repo_name}: {e}")
        else:
            # Global search across all of GitHub matching user labels
            issues_data = self._global_search_issues(labels=config.search_labels, limit=15)

        return issues_data

    def _fetch_repo_issues(self, repo_name: str, labels: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        issues_data = []
        seen = set()
        primary_label = labels[0] if labels else "good first issue"

        if self._github:
            repo = self._github.get_repo(repo_name)
            open_issues = repo.get_issues(state="open", labels=[primary_label], sort="created", direction="desc")
            count = 0
            for issue in open_issues:
                if issue.pull_request or str(issue.id) in seen:
                    continue
                seen.add(str(issue.id))
                issues_data.append({
                    "id": str(issue.id),
                    "title": issue.title,
                    "url": issue.html_url,
                    "description": issue.body or "",
                    "repository": repo_name,
                    "labels": [label.name for label in issue.labels],
                    "created_at": issue.created_at.isoformat(),
                    "comments_count": issue.comments,
                })
                count += 1
                if count >= limit:
                    break
        else:
            headers = {"Accept": "application/vnd.github+json"}
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"

            url = f"https://api.github.com/repos/{repo_name}/issues?state=open&labels={requests.utils.quote(primary_label)}&sort=created&direction=desc&per_page={limit}"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                for item in response.json():
                    if "pull_request" in item or str(item["id"]) in seen:
                        continue
                    seen.add(str(item["id"]))
                    issues_data.append({
                        "id": str(item["id"]),
                        "title": item["title"],
                        "url": item["html_url"],
                        "description": item.get("body") or "",
                        "repository": repo_name,
                        "labels": [l["name"] for l in item.get("labels", [])],
                        "created_at": item.get("created_at", ""),
                        "comments_count": item.get("comments", 0),
                    })
        return issues_data

    def _global_search_issues(self, labels: List[str], limit: int = 15) -> List[Dict[str, Any]]:
        issues_data = []
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        primary_label = labels[0] if labels else "good first issue"
        query = f'label:"{primary_label}" state:open is:issue'
        url = f"https://api.github.com/search/issues?q={requests.utils.quote(query)}&sort=created&order=desc&per_page={limit}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                items = response.json().get("items", [])
                for item in items:
                    repo_url = item.get("repository_url", "")
                    repo_name = repo_url.replace("https://api.github.com/repos/", "")
                    issues_data.append({
                        "id": str(item["id"]),
                        "title": item["title"],
                        "url": item["html_url"],
                        "description": item.get("body") or "",
                        "repository": repo_name,
                        "labels": [l["name"] for l in item.get("labels", [])],
                        "created_at": item.get("created_at", ""),
                        "comments_count": item.get("comments", 0),
                    })
        except Exception as e:
            print(f"Failed global GitHub search: {e}")

        return issues_data
