"""
Service module
"""
import hashlib

from github import Github
from github.Repository import Repository


def calc_score(stargazers_count: int, forks_count: int) -> int:
    """Check repo popularity"""
    return (stargazers_count + (forks_count * 2))


def is_popular(score: int) -> bool:
    """Check repo popularity"""
    return score >= 500


def get_repo(g: Github, owner: str, repo: str) -> Repository:
    """Retrieve a repo info"""
    return g.get_repo(f"{owner}/{repo}")


def make_cache_key(url: str):
    return f"cache_{hashlib.sha1(url.encode('utf-8')).hexdigest()}"
