from fastapi import APIRouter, status
from contracts.requests.auth_request import AuthenticationRequest
from contracts.responses.auth_response import AuthenticationResponse
from contracts.responses.base import ProblemResponse
from core.application.users.auth.login import login as login_service
from core.infrastructure.database.manage import DbSession

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
