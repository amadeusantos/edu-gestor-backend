from typing import Callable, Optional, TypeVar
from sqlalchemy.orm import scoped_session
from core.infrastructure.database.engine import DatabaseEngine


class LazySessionHolder:
    def __init__(self, engine: DatabaseEngine) -> None:
        self.session: Optional[scoped_session] = engine.get_session()

    def commit(self) -> None:
        if not self.session:
            raise Exception("Session is not initialized.")
        self.session.commit()

    def rollback(self) -> None:
        if not self.session:
            raise Exception("Session is not initialized.")
        self.session.rollback()

    def close(self) -> None:
        if self.session:
            self.session.close()
            self.session = None


T = TypeVar("T")


def db_session(func: Callable[..., T]) -> Callable[..., T]:
    def wrapper(*args, **kwargs):
        engine = kwargs.get("engine")
        if type(engine) != DatabaseEngine:
            raise TypeError("engine must be of type DatabaseEngine")
        session_holder = LazySessionHolder(engine)
        try:
            response = func(*args, **kwargs, session_holder=session_holder)
            return response
        except Exception as e:
            session_holder.rollback()
            raise e
        finally:
            session_holder.close()

    return wrapper


def get_session(**kwargs) -> scoped_session:
    if "session_holder" not in kwargs:
        raise KeyError("session holder parameter is required")

    if type(kwargs["session_holder"]) != LazySessionHolder:
        raise TypeError("session holder parameter must be of type LazySessionHolder")

    if not kwargs["session_holder"].session:
        raise ValueError("session holder parameter must be initialized")

    return kwargs["session_holder"].session
