from uuid import UUID

import bcrypt
from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session

from api.authentication import Authorizations
from api.database import pagination
from api.schemas import UserPrincipal
from api.user.exceptions import UserNotFoundException
from api.user.schemas import UserCreateSchema, UserPaginationSchema, UserSchema, UserUpdateSchema
from api.user.validations import validate_create_user, validate_update_user
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.enums import RoleEnum
from infrastructure.persistence.models import UserModel

router = APIRouter(prefix="/users", tags=["Users"])


def query_users(session: Session):
    return session.query(UserModel)


def query_first(session: Session, id: UUID):
    query = query_users(session)
    user = query.where(UserModel.id == id).first()

    if not user:
        raise UserNotFoundException()

    return user


def query_user_by_email(session: Session, email: str):
    query = query_users(session)
    user = query.where(UserModel.email == email).first()

    if not user:
        raise UserNotFoundException()

    return user

def user_model(user_dto: UserCreateSchema, user: UserModel):
    match user_dto.role:
        case RoleEnum.ADMIN:
            user.student_id = None
            user.professor_id = None
        case RoleEnum.COORDINATOR:
            user.student_id = None
            user.professor_id = None
        case RoleEnum.PROFESSOR:
            user.student_id = None
            user.professor_id = user_dto.professor_id
        case RoleEnum.STUDENT:
            user.student_id = user_dto.student_id
            user.professor_id = None
        case RoleEnum.RESPONSIBLE:
            user.student_id = user_dto.student_id
            user.professor_id = None
    return user


@router.get("")
def users_pagination(
        page: int = 1,
        size: int = 10,
        search: str | None = Query(None),
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN]))
) -> UserPaginationSchema:
    query = query_users(session)
    filters = []

    if search:
        filters.append(UserModel.email.icontains(search))

    orders = [UserModel.enabled.desc()]

    return pagination(query, page, size, filters, orders)


@router.get("/email/{email}")
def get_user_by_email(
        email: str,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN]))
) -> UserSchema:
    return query_user_by_email(session, email)


@router.get("/{id}")
def get_user(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN]))
) -> UserSchema:
    return query_first(session, id)


@router.post("", status_code=204)
def create_user(
        dto: UserCreateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN]))
):
    validate_create_user(session, dto)
    password_hash = bcrypt.hashpw(dto.password.encode(), bcrypt.gensalt())
    user = UserModel(
        email=dto.email,
        password=password_hash,
        role=dto.role,
    )
    user_model(dto, user)
    session.add(user)
    session.commit()
    return {}


@router.put("/{id}")
def update_user(
        id: UUID,
        dto: UserUpdateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN]))
) -> UserSchema:
    user = query_first(session, id)
    validate_update_user(session, dto, user.id)
    user.email = dto.email
    user.role = dto.role
    user_model(dto, user)
    if dto.password:
        password_hash = bcrypt.hashpw(dto.password.encode(), bcrypt.gensalt())
        user.password = password_hash
    session.flush()
    session.commit()
    session.refresh(user)
    return user


@router.patch("/{id}")
def update_user_enabled(
        id: UUID, enabled: bool,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN]))
) -> UserSchema:
    user = query_first(session, id)
    session.query(UserModel).where(UserModel.id == user.id).update({"enabled": enabled})
    session.flush()
    session.commit()
    session.refresh(user)
    return user
