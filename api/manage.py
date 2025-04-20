import os
from contextlib import asynccontextmanager
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import main_router
from core.infrastructure.database.engine import DatabaseEngine
from core.infrastructure.security.super_user import create_super_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Engine initialization
    app.state.db_engine = DatabaseEngine()
    
    # Migrations initialization
    config_ini_file = f"{os.getcwd()}/alembic.ini"
    alembic_cfg = Config(config_ini_file)
    command.upgrade(alembic_cfg, "head")
    
    # Super user initialization
    create_super_user(engine=app.state.db_engine)

    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)
