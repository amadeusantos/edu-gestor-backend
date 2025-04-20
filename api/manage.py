from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import main_router
from core.infrastructure.database.engine import DatabaseEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_engine = DatabaseEngine()
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
