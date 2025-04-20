from fastapi import APIRouter, Request, status
from contracts.requests.auth_request import AuthenticationRequest
from contracts.responses.auth_response import AuthenticationResponse
from contracts.responses.base import ProblemResponse
from core.application.users.auth.login import login as login_service

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=AuthenticationResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ProblemResponse},
    },
)
def login(
    request_body: AuthenticationRequest, request: Request
) -> AuthenticationResponse:
    return login_service(request_body, engine=request.app.state.db_engine)
