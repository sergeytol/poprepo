"""
Main module
"""
import json
from typing import Optional

import aioredis
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

redis_client = aioredis.from_url(
    f"redis://{Settings.POPREPO_REDIS_HOST}:{Settings.POPREPO_REDIS_PORT}"
    f"?password={Settings.POPREPO_REDIS_PASSWORD}",
    decode_responses=True
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
    cached = await redis_client.hgetall(make_cache_key(request.url.path))
    if cached:
        return JSONResponse(
            status_code=int(cached["status_code"]),
            content=json.loads(cached["body"]),
        )

    response = await call_next(request)

    # save to cache
    if response.status_code > status.HTTP_300_MULTIPLE_CHOICES:
        return response

    response_body = [section async for section in response.__dict__["body_iterator"]]
    decoded_body = response_body[0].decode()
    redis_key = make_cache_key(request.url.path)
    await redis_client.hset(
        redis_key,
        mapping={"status_code": response.status_code, "body": decoded_body}
    )
    await redis_client.expire(redis_key, Settings.POPREPO_FEATURE_CACHE_TTL_SEC)

    return JSONResponse(
        content=json.loads(decoded_body),
        status_code=response.status_code
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
