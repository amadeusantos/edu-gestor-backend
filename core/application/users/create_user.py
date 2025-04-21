from sqlalchemy.orm import Session
from contracts.requests.user_request import CreateUserRequest
from contracts.responses.user_response import UserResponse
from core.infrastructure.security.password import hash_password


def create_user(user_request: CreateUserRequest, db_session: Session):
    user = user_request.to_row()
    user.password = hash_password(user_request.password)
    db_session.add(user)
    db_session.flush()

    return UserResponse.from_row(user)
