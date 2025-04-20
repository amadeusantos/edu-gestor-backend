from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query, Depends
from sqlalchemy.orm import Session

from api.authentication import Authorizations
from api.database import pagination
from api.discipline.exceptions import DisciplineNotFoundException
from api.discipline.schemas import DisciplinePaginationSchema, DisciplineSchema, DisciplineCreateSchema, \
    DisciplineUpdateSchema
from api.schemas import UserPrincipal
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.enums import RoleEnum
from infrastructure.persistence.models import DisciplineModel

router = APIRouter(prefix="/disciplines", tags=["Discipline"])


def query_disciplines(session: Session):
    return session.query(DisciplineModel).where(DisciplineModel.deleted == False)


def query_first(session: Session, id: UUID):
    query = query_disciplines(session)
    discipline = query.where(DisciplineModel.id == id).first()

    if not discipline:
        raise DisciplineNotFoundException()

    return discipline


@router.get("")
def disciplines_pagination(
        search: str | None = Query(default=None),
        page: int = 1,
        size: int = 10,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> DisciplinePaginationSchema:
    query = query_disciplines(session)
    filters = []

    if search:
        filters.append(DisciplineModel.name.icontains(search))

    orders = [DisciplineModel.archived.desc()]

    return pagination(query, page, size, filters, orders)


@router.get("/{id}")
def get_discipline(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> DisciplineSchema:
    return query_first(session, id)


@router.post("")
def create_discipline(
        dto: DisciplineCreateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> DisciplineSchema:
    discipline = DisciplineModel(**dto.model_dump())
    session.add(discipline)
    session.commit()
    session.refresh(discipline)
    return discipline


@router.put("/{id}")
def update_student(
        id: UUID,
        dto: DisciplineUpdateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> DisciplineSchema:
    discipline = query_first(session, id)
    session.query(DisciplineModel).where(DisciplineModel.id == discipline.id).update(dto.model_dump())
    session.commit()
    session.refresh(discipline)
    return discipline


@router.delete("/{id}", status_code=204)
def delete_discipline(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
):
    discipline = query_first(session, id)
    session.query(DisciplineModel).where(DisciplineModel.id == discipline.id).update({"deleted": True})
    session.commit()
    return {}
