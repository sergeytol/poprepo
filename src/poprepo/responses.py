"""
Response models collection
"""
from pydantic.main import BaseModel


class PingResponse(BaseModel):
    pong: bool = True


class RepoPopularityResponse(BaseModel):
    is_popular: bool
