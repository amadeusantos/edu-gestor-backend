from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query, Depends
from sqlalchemy.orm import Session

from api.authentication import Authorizations
from api.database import pagination
from api.frequency.actions import sync_students
from api.frequency.exceptions import FrequencyNotFoundException
from api.frequency.schemas import FrequencyPaginationSchema, FrequencySchema, FrequencyCreateSchema, \
    FrequencyUpdateSchema
from api.schemas import UserPrincipal
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.enums import RoleEnum
from infrastructure.persistence.models import FrequencyModel

router = APIRouter(prefix="/frequencies", tags=["Frequency Diary"])


def query_frequencies(session: Session):
    return session.query(FrequencyModel).where(FrequencyModel.deleted == False)


def query_first(session: Session, id: UUID):
    query = query_frequencies(session)
    discipline = query.where(FrequencyModel.id == id).first()

    if not discipline:
        raise FrequencyNotFoundException()

    return discipline


@router.get("")
def frequencies_pagination(
        discipline_id: UUID | None = Query(default=None),
        page: int = 1,
        size: int = 10,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> FrequencyPaginationSchema:
    query = query_frequencies(session)
    filters = []

    if discipline_id:
        filters.append(FrequencyModel.discipline_id == discipline_id)

    orders = [FrequencyModel.archived.desc()]

    return pagination(query, page, size, filters, orders)


@router.get("/{id}")
def get_frequency(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> FrequencySchema:
    return query_first(session, id)


@router.post("")
def create_frequency(
        dto: FrequencyCreateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> FrequencySchema:
    frequency = FrequencyModel(**dto.model_dump(exclude={"presents_ids"}))
    session.add(frequency)
    session.flush()
    sync_students(session, frequency, dto.presents_ids)
    session.commit()
    session.refresh(frequency)
    return frequency


@router.put("/{id}")
def update_frequency(
        id: UUID,
        dto: FrequencyUpdateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> FrequencySchema:
    frequency = query_first(session, id)
    sync_students(session, frequency, dto.presents_ids)
    session.commit()
    session.refresh(frequency)
    return frequency


@router.delete("/{id}", status_code=204)
def delete_frequency(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
):
    frequency = query_first(session, id)
    session.query(FrequencyModel).where(FrequencyModel.id == frequency.id).update({"deleted": True})
    session.commit()
    return {}
