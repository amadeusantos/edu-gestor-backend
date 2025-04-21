# import os
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Final, Optional
from uuid import uuid1
# from alembic import command
# from alembic.config import Config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import scoped_session, sessionmaker
from api.routes import main_router
from core.infrastructure.database.manage import engine
# from core.infrastructure.security.super_user import create_super_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: Migrations initialization
    # config_ini_file = f"{os.getcwd()}/alembic.ini"
    # alembic_cfg = Config(config_ini_file)
    # command.upgrade(alembic_cfg, "head")

    # TODO: Super user initialization
    # create_super_user(engine=app.state.db_engine)

    yield


app = FastAPI(lifespan=lifespan)

REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None
)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())

    ctx_token = _request_id_ctx_var.set(request_id)
    session = None

    try:
        session = scoped_session(sessionmaker(bind=engine), scopefunc=get_request_id)
        request.state.db = session()

        response = await call_next(request)

        if hasattr(request.state, "db") and request.state.db.is_active:
            request.state.db.commit()

        return response

    except Exception as e:
        try:
            if hasattr(request.state, "db") and request.state.db.is_active:
                request.state.db.rollback()
        except Exception as rollback_error:
            print(
                f"Error during rollback: {rollback_error}"
            )  # TODO: add logging.error()

        raise e from None
    finally:
        if hasattr(request.state, "db"):
            try:
                request.state.db.close()
                if session is not None:
                    session.remove()
            except Exception as close_error:
                print(
                    f"Error closing database session: {close_error}"
                )  # TODO: add logging.error()

        _request_id_ctx_var.reset(ctx_token)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
