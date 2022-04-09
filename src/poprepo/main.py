"""
Main module
"""
import json
from typing import Optional

import redis
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from github import Github
from github.GithubException import (BadCredentialsException,
                                    UnknownObjectException)
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from poprepo.service import get_repo, is_popular, make_cache_key
from poprepo.settings import Settings


app = FastAPI()

redis_client = redis.Redis(
    host=Settings.POPREPO_REDIS_HOST,
    port=Settings.POPREPO_REDIS_PORT,
    password=Settings.POPREPO_REDIS_PASSWORD,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """HTTP middleware / caching"""
    if (
        not Settings.POPREPO_FEATURE_CACHE_ENABLED
        or request.headers.get("X-Use-Caching") != "on"
    ):
        response = await call_next(request)
        return response

    # read from cache
    cached = redis_client.hgetall(make_cache_key(request.url.path))
    print(cached)
    if cached:
        print("it's from cache")
        return JSONResponse(
            status_code=int(cached[b"status_code"].decode()),
            content=json.loads(cached[b"body"].decode()),
        )

    response = await call_next(request)

    # write to cache
    if response.status_code > status.HTTP_300_MULTIPLE_CHOICES:
        return response

    response_body = [section async for section in response.__dict__["body_iterator"]]
    decoded_body = response_body[0].decode()
    redis_key = make_cache_key(request.url.path)
    redis_client.hset(
        redis_key, mapping={"status_code": response.status_code, "body": decoded_body}
    )
    redis_client.expire(redis_key, Settings.POPREPO_FEATURE_CACHE_TTL_SEC)

    return JSONResponse(
        content=json.loads(decoded_body), status_code=response.status_code
    )


@app.get("/ping")
async def ping():
    """Ping/pong for a quick check"""
    return {"pong": True}


@app.get("/repo/{owner}/{repo}/popularity")
async def endpoint_popularity(
    owner: str,
    repo: str,
    x_use_caching: Optional[str] = Header(None),
    github_access_token: str = Header(None),
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
        log_level=Settings.POPREPO_LOG_LEVEL,
        reload=Settings.POPREPO_LIVE_RELOAD,
    )
