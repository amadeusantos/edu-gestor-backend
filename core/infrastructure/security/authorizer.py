from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.infrastructure.database.manage import get_db
from core.infrastructure.database.tables import RoleEnum, User
from core.infrastructure.environment.manage import settings


def get_current_user(
    authorization: Annotated[
        HTTPAuthorizationCredentials | None, Depends(HTTPBearer())
    ],
    session: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if authorization is None:
        raise credentials_exception

    try:
        payload = jwt.decode(
            authorization.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("sub")
    except Exception:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == username))
    if user is None:
        raise credentials_exception

    return user


class Authorizer:
    def __init__(self, roles: list[RoleEnum]):
        self.roles = roles

    def __call__(self, current_user=Depends(get_current_user)):
        if not current_user.role in [role for role in self.roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user
