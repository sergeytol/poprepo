from os import getenv
from pathlib import Path

import environ
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from github import Github
from github.GithubException import (BadCredentialsException,
                                    UnknownObjectException)
from github.Repository import Repository

ROOT_DIR = Path(__file__).resolve().parent.parent

env_name = getenv("ENVIO_SETTINGS_ENV", "dev")
env = environ.Env()
env.read_env(ROOT_DIR / f"env/.env.{env_name}")

app = FastAPI()


def error_response(message: str):
    """Wrapper for error responses"""
    return {"detail": message}


def is_popular(stargazers_count: int, forks_count: int) -> bool:
    """Check repo popularity"""
    return (stargazers_count + (forks_count * 2)) >= 500


def get_repo(g: Github, owner: str, repo: str) -> Repository:
    """Retrieve a repo info"""
    return g.get_repo(f"{owner}/{repo}")


@app.get("/ping")
async def ping():
    """Ping/pong for a quick check"""
    return {"pong": True}


@app.get("/repo/{owner}/{repo}/popularity")
async def endpoint_popularity(
    owner: str, repo: str, github_access_token: str = Header(None)
):
    """Checking a repo popularity. It requires GitHub-Access-Token header"""
    if not github_access_token:
        raise HTTPException(status_code=400, detail="Access token is required")

    github_api = Github(github_access_token)

    try:
        repo = get_repo(github_api, owner, repo)
    except UnknownObjectException:
        raise HTTPException(
            status_code=404, detail="Repository not found or is private"
        )
    except BadCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid access token")

    return {"is_popular": is_popular(repo.stargazers_count, repo.forks)}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        log_level=env.str("POPREPO_LOG_LEVEL", default="error"),
        reload=env.bool("POPREPO_LIVE_RELOAD", default=False),
    )
