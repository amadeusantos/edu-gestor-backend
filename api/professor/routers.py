from uuid import UUID

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from api.authentication import Authorizations
from api.database import pagination
from api.professor.actions import actions_delete_professor
from api.professor.exceptions import ProfessorNotFoundException
from api.professor.schemas import ProfessorPaginationSchema, ProfessorCreateSchema, ProfessorSchema, \
    ProfessorUpdateSchema
from api.professor.validations import validate_create_professor, validate_update_professor
from api.schemas import UserPrincipal
from api.utils import format_cpf
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.enums import RoleEnum
from infrastructure.persistence.models import ProfessorModel

router = APIRouter(prefix="/professors", tags=["Professor"])


def query_professors(session: Session):
    return session.query(ProfessorModel).where(ProfessorModel.deleted == False)


def query_first(session: Session, id: UUID):
    query = query_professors(session)
    professor = query.where(ProfessorModel.id == id).first()
    if not professor:
        raise ProfessorNotFoundException()
    return professor


def query_professor_by_cpf(session: Session, cpf: str):
    query = query_professors(session)
    professor = query.where(ProfessorModel.cpf == cpf).first()
    if not professor:
        raise ProfessorNotFoundException()
    return professor


@router.get("")
def professors_pagination(
        search: str | None = Query(default=None),
        page: int = 1,
        size: int = 10,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> ProfessorPaginationSchema:
    query = query_professors(session)
    filters = []

    if search:
        filters.append(ProfessorModel.fullname.icontains(search))

    orders = [ProfessorModel.archived.desc(), ProfessorModel.fullname]

    return pagination(query, page, size, filters, orders)


@router.get("/cpf/{cpf}")
def get_professor_by_cpf(
        cpf: str,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> ProfessorSchema:
    cpf = format_cpf(cpf)
    return query_professor_by_cpf(session, cpf)


@router.get("/{id}")
def get_professor(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> ProfessorSchema:
    return query_first(session, id)


@router.post("")
def create_professor(
        dto: ProfessorCreateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> ProfessorSchema:
    validate_create_professor(session, dto)
    professor = ProfessorModel(**dto.model_dump())
    session.add(professor)
    session.commit()
    session.refresh(professor)
    return professor


@router.put("/{id}")
def update_professor(
        id: UUID,
        dto: ProfessorUpdateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> ProfessorSchema:
    professor = query_first(session, id)
    validate_update_professor(session, dto, professor.id)
    session.query(ProfessorModel).where(ProfessorModel.id == professor.id).update(dto.model_dump())
    session.commit()
    session.refresh(professor)
    return professor


@router.delete("/{id}", status_code=204)
def delete_professor(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
):
    professor = query_first(session, id)
    session.query(ProfessorModel).where(ProfessorModel.id == professor.id).update({"deleted": True})
    actions_delete_professor(session, id)
    session.commit()
    return {}
