"""
Response models collection
"""
from datetime import datetime

from pydantic.main import BaseModel


class PingResponse(BaseModel):
    pong: bool = True


class RepoPopularityResponse(BaseModel):
    is_popular: bool
    score: int
    stargazers_count: int
    forks: int
    private: bool
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime


class ErrorResponse(BaseModel):
    detail: str
