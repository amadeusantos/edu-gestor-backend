from typing import Annotated
from fastapi import APIRouter, Depends, status
from contracts.requests.auth_request import AuthenticationRequest
from contracts.responses.auth_response import (
    AuthenticationResponse,
    CurrentUserResponse,
)
from contracts.responses.base import ProblemResponse
from core.application.users.auth.login import login as login_service
from core.infrastructure.database.manage import DbSession
from core.infrastructure.database.tables import User
from core.infrastructure.security.authorizer import get_current_user

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=AuthenticationResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ProblemResponse},
    },
)
def login(
    login_request: AuthenticationRequest, db_session: DbSession
) -> AuthenticationResponse:
    return login_service(login_request, db_session)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=CurrentUserResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ProblemResponse},
    },
)
def get_authenticated_user(
    _: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> CurrentUserResponse:
    return CurrentUserResponse.from_row(current_user)
