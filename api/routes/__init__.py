from fastapi import APIRouter
from api.routes.authentication_router import router as authentication_router
from api.routes.health_check_router import router as health_check_router
from api.routes.profile_router import router as profile_router
from api.routes.user_router import router as user_router

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

main_router.include_router(
    user_router,
    prefix="/users",
    tags=["users"],
)

main_router.include_router(
    profile_router,
    prefix="/profiles",
    tags=["profiles"],
)
