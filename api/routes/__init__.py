from fastapi import APIRouter
from api.routes.health_check_router import router as health_check_router

main_router = APIRouter()

main_router.include_router(
    health_check_router,
    prefix="/health",
    tags=["health check"],
)
