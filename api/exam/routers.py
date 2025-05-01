from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session

from api.authentication import Authorizations
from api.database import pagination
from api.exam.actions import sync_students, create_activity, update_activity
from api.exam.exceptions import ExamNotFoundException
from api.exam.schemas import ExamPaginationSchema, ExamSchema, ExamCreateSchema, ExamUpdateSchema
from api.schemas import UserPrincipal
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.enums import RoleEnum
from infrastructure.persistence.models import ExamModel

router = APIRouter(prefix="/exams", tags=["Exam"])


def query_exams(session: Session):
    return session.query(ExamModel).where(ExamModel.deleted == False)


def query_first(session: Session, id: UUID):
    query = query_exams(session)
    exam = query.where(ExamModel.id == id).first()

    if not exam:
        raise ExamNotFoundException()

    return exam


@router.get("")
def exams_pagination(
        discipline_id: UUID | None = Query(default=None),
        page: int = 1,
        size: int = 10,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations(
                [RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR, RoleEnum.STUDENT, RoleEnum.RESPONSIBLE]))
) -> ExamPaginationSchema:
    query = query_exams(session)
    filters = []

    if discipline_id:
        filters.append(ExamModel.discipline_id == discipline_id)

    orders = [ExamModel.archived.desc(), ExamModel.date.desc(), ExamModel.is_finish]

    return pagination(query, page, size, filters, orders)


@router.get("/{id}")
def get_exam(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations(
                [RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR, RoleEnum.STUDENT, RoleEnum.RESPONSIBLE]))
) -> ExamSchema:
    return query_first(session, id)

@router.post("")
def create_exam(
        dto: ExamCreateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations(
                [RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> ExamSchema:
    exam = ExamModel(**dto.model_dump())
    session.add(exam)
    session.flush()
    sync_students(session, exam)
    create_activity(session, exam)
    session.commit()
    session.refresh(exam)
    return exam


@router.put("/{id}")
def update_exam(
        id: UUID,
        dto: ExamUpdateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> ExamSchema:
    exam = query_first(session, id)
    session.query(ExamModel).where(ExamModel.id == exam.id).update(dto.model_dump())
    session.flush()
    sync_students(session, exam)
    session.refresh(exam)
    update_activity(session, exam)
    session.commit()
    session.refresh(exam)
    return exam


@router.delete("/{id}", status_code=204)
def delete_exam(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
):
    exam = query_first(session, id)
    session.query(ExamModel).where(ExamModel.id == exam.id).update({"deleted": True})
    session.commit()
    return {}