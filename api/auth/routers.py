from datetime import datetime, timezone, timedelta

import bcrypt
import jwt
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.auth.schemas import AuthenticationSchema, TokenSchema, AuthenticatedSchema
from api.authentication import authenticated
from api.schemas import UserPrincipal
from config.settings import envSettings
from api.exceptions import NotAuthenticated
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.models import UserModel

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: AuthenticationSchema, session: Session = Depends(open_db_session)) -> TokenSchema:
    user = session.query(UserModel).where(UserModel.enabled == True, UserModel.email == data.email).first()
    if not (user and bcrypt.checkpw(data.password.encode(), user.password)):
        raise NotAuthenticated()

    token = jwt.encode({"sub": str(user.id), "role": user.role.value, 'iat': datetime.now(timezone.utc),
                        'exp': datetime.now(timezone.utc) + timedelta(days=1)}, envSettings.SECRET_KEY,
                       algorithm="HS256")
    return TokenSchema(token=token)


@router.get("/authenticated")
def authenticated_user(
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(authenticated)
) -> AuthenticatedSchema:
    return session.query(UserModel).where(UserModel.id == user_principal.id).first()
