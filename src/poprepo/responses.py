from pydantic.main import BaseModel


class PingResponse(BaseModel):
    pong: bool = True
