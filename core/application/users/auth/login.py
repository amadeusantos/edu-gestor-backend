from fastapi import HTTPException, status
from contracts.requests.auth_request import AuthenticationRequest
from contracts.responses.auth_response import AuthenticationResponse
from core.infrastructure.database.session import db_session, get_session
from core.infrastructure.database.tables import User
from core.infrastructure.security.jwt import create_access_token
from core.infrastructure.security.password import verify_password


@db_session
def login(request_body: AuthenticationRequest, **kwargs) -> AuthenticationResponse:
    session = get_session(**kwargs)

    if (
        user := session.query(User).filter_by(email=request_body.email).first()
    ) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(request_body.password, user.password):
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
