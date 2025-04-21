from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.requests import Request
from core.infrastructure.environment.manage import settings

engine = create_engine(
    settings.DB_URI,
)


def get_db(request: Request) -> Session:
    return request.state.db


DbSession = Annotated[Session, Depends(get_db)]
