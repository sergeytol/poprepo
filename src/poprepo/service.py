"""
Service module
"""
import hashlib

from github import Github
from github.Repository import Repository


def error_response(message: str):
    """Wrapper for error responses"""
    return {"detail": message}


def is_popular(stargazers_count: int, forks_count: int) -> bool:
    """Check repo popularity"""
    return (stargazers_count + (forks_count * 2)) >= 500


def get_repo(g: Github, owner: str, repo: str) -> Repository:
    """Retrieve a repo info"""
    return g.get_repo(f"{owner}/{repo}")


def make_cache_key(url: str):
    return f"cache_{hashlib.sha1(url.encode('utf-8')).hexdigest()}"
