from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from core.infrastructure.database.tables import Base
from core.infrastructure.environment.manage import settings


class DatabaseEngine:
    def __init__(self) -> None:
        self.engine: Optional[Engine] = create_engine(settings.DB_URI)
        Base.metadata.bind = self.engine

    def get_session(self) -> scoped_session:
        if not self.engine:
            raise Exception("Database engine is not initialized.")

        return scoped_session(sessionmaker(bind=self.engine))

    def close_engine(self) -> None:
        if self.engine:
            self.engine.dispose()
            self.engine = None
