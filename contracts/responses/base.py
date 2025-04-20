from pydantic import BaseModel


class ProblemResponse(BaseModel):
    detail: str
