from typing import Annotated, List

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from api.exceptions import TokenInvalidException, ForbiddenException
from api.schemas import UserPrincipal
from config.settings import envSettings
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.enums import RoleEnum
from infrastructure.persistence.models import UserModel


def authenticated(
        authorization: Annotated[HTTPAuthorizationCredentials | None, Depends(HTTPBearer())],
        session: Session = Depends(open_db_session)
):
    try:
        payload = jwt.decode(authorization.credentials, envSettings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub", "")
        user = session.query(UserModel).where(UserModel.id == user_id).first()
        if user is None:
            raise TokenInvalidException()
        return UserPrincipal(
            id=user.id,
            role=user.role,
            student_id=user.student_id,
            professor_id=user.professor_id,
        )
    except (jwt.InvalidTokenError, ValidationError, KeyError):
        raise TokenInvalidException()


class Authorizations:
    def __init__(self, roles: List[RoleEnum] | None = None):
        self.roles = roles

    def __call__(self, user_principal: UserPrincipal = Depends(authenticated)):
        if user_principal.role in [r.value for r in self.roles]:
            return user_principal
        raise ForbiddenException()
