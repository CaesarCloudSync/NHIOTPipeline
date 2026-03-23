from pydantic import BaseModel


class CommandResponse(BaseModel):
    result: str
    error: str
    