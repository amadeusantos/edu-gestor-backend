from fastapi import HTTPException, status
from contracts.requests.auth_request import AuthenticationRequest
from contracts.responses.auth_response import AuthenticationResponse
from core.infrastructure.database.manage import DbSession
from core.infrastructure.database.tables import User
from core.infrastructure.security.jwt import create_access_token
from core.infrastructure.security.password import verify_password


def login(
    login_request: AuthenticationRequest, db_session: DbSession
) -> AuthenticationResponse:
    if (
        user := db_session.query(User).filter_by(email=login_request.email).first()
    ) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(login_request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token, exp_time = create_access_token(user.email)

    return AuthenticationResponse.from_row(
        row=user,
        access_token=access_token,
        exp_time=exp_time,
    )
