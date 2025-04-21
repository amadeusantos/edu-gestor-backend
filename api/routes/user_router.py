from typing import Annotated
from fastapi import APIRouter, Depends, status
from contracts.requests.user_request import CreateUserRequest
from contracts.responses.base import ProblemResponse
from contracts.responses.user_response import UserResponse
from core.application.users.create_user import create_user as create_user_service
from core.infrastructure.database.manage import DbSession
from core.infrastructure.database.tables import RoleEnum, User
from core.infrastructure.security.authorizer import Authorizer

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ProblemResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ProblemResponse},
        status.HTTP_403_FORBIDDEN: {"model": ProblemResponse},
        status.HTTP_409_CONFLICT: {"model": ProblemResponse},
    },
)
def create_user(
    create_user_request: CreateUserRequest,
    db_session: DbSession,
    current_user: Annotated[User, Depends(Authorizer([RoleEnum.ADMIN]))],
) -> UserResponse:
    return create_user_service(create_user_request, db_session)
