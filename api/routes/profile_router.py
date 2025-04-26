from typing import Annotated
from fastapi import APIRouter, Depends, status
from contracts.requests.user_request import CreateProfileRequest
from contracts.responses.base import ProblemResponse
from contracts.responses.user_response import ProfileResponse
from core.application.users.profiles.create_profile import (
    create_profile as create_profile_service,
)
from core.infrastructure.database.manage import DbSession
from core.infrastructure.database.tables import RoleEnum, User
from core.infrastructure.security.authorizer import Authorizer

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ProfileResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ProblemResponse},
        status.HTTP_403_FORBIDDEN: {"model": ProblemResponse},
        status.HTTP_409_CONFLICT: {"model": ProblemResponse},
    },
)
def create_profile(
    create_profile_request: CreateProfileRequest,
    db_session: DbSession,
    current_user: Annotated[
        User, Depends(Authorizer([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
    ],
) -> ProfileResponse:
    return create_profile_service(create_profile_request, db_session)
