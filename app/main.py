from os import getenv

import environ
from github import Github
from fastapi import FastAPI, Header, HTTPException
from pathlib import Path
import uvicorn
from github.GithubException import UnknownObjectException, BadCredentialsException

ROOT_DIR = Path(__file__).resolve().parent.parent

env_name = getenv('ENVIO_SETTINGS_ENV', 'dev')
env = environ.Env()
env.read_env(ROOT_DIR / f'env/.env.{env_name}')

app = FastAPI()


def error_response(message: str):
    return {"detail": message}


def is_popular(stargazers_count: int, forks_count: int) -> bool:
    return (stargazers_count + (forks_count * 2)) >= 500


@app.get("/ping")
async def ping():
    return {"pong": True}


@app.get("/repo/{owner}/{repo}/popularity")
async def endpoint_popularity(
        owner: str,
        repo: str,
        github_access_token: str = Header(None)
):
    if not github_access_token:
        raise HTTPException(status_code=400, detail="Access token is required")

    g = Github(github_access_token)

    try:
        repo = g.get_repo(f"{owner}/{repo}")
    except UnknownObjectException:
        raise HTTPException(status_code=404, detail="Repository not found or is private")
    except BadCredentialsException as exc:
        raise HTTPException(status_code=401, detail="Invalid access token")

    return {"is_popular": is_popular(int(repo.stargazers_count), int(repo.forks))}


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=80,
                log_level=env.str('POPREPO_LOG_LEVEL', default='error'),
                reload=env.bool('POPREPO_LIVE_RELOAD', default=False))
