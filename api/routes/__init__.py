from fastapi import APIRouter
from api.routes.authentication_router import router as authentication_router
from api.routes.health_check_router import router as health_check_router

main_router = APIRouter()

main_router.include_router(
    authentication_router,
    prefix="/auth",
    tags=["authentication"],
)

main_router.include_router(
    health_check_router,
    prefix="/health",
    tags=["health check"],
)
