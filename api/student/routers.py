from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session

from api.authentication import Authorizations
from api.database import pagination
from api.schemas import UserPrincipal
from api.student.exceptions import StudentNotFoundException
from api.student.schemas import StudentCreateSchema, StudentSchema, StudentUpdateSchema, StudentPaginationSchema
from api.student.validations import validate_create_student, validate_update_student
from api.utils import format_cpf
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.enums import RoleEnum
from infrastructure.persistence.models import StudentModel

router = APIRouter(prefix="/students", tags=["Student"])


def query_students(session: Session):
    return session.query(StudentModel).where(StudentModel.deleted == False)


def query_first(session: Session, id: UUID):
    query = query_students(session)
    student = query.where(StudentModel.id == id).first()

    if not student:
        raise StudentNotFoundException()

    return student

def query_student_by_cpf(session: Session, cpf: str):
    query = query_students(session)
    student = query.where(StudentModel.cpf == cpf).first()

    if not student:
        raise StudentNotFoundException()

    return student


@router.get("")
def students_pagination(
        page: int = 1,
        size: int = 10,
        search: str | None = Query(default=None),
        classroom_id: UUID | None = Query(default=None),
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> StudentPaginationSchema:
    query = query_students(session)
    filters = []

    if search:
        filters.append(StudentModel.fullname.icontains(search))

    orders = [StudentModel.archived.desc(), StudentModel.fullname]

    return pagination(query, page, size, filters, orders)

@router.get("/cpf/{cpf}")
def get_student(
        cpf: str,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> StudentSchema:
    cpf = format_cpf(cpf)
    return query_student_by_cpf(session, cpf)

@router.get("/{id}")
def get_student(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> StudentSchema:
    return query_first(session, id)


@router.post("")
def create_student(
        dto: StudentCreateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> StudentSchema:
    validate_create_student(session, dto)
    student = StudentModel(**dto.model_dump())
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@router.put("/{id}")
def update_student(
        id: UUID,
        dto: StudentUpdateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> StudentSchema:
    student = query_first(session, id)
    validate_update_student(session, dto, student.id)
    session.query(StudentModel).where(StudentModel.id == student.id).update(dto.model_dump())
    session.commit()
    session.refresh(student)
    return student


@router.delete("/{id}", status_code=204)
def delete_student(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
):
    student = query_first(session, id)
    session.query(StudentModel).where(StudentModel.id == student.id).update({"deleted": True})
    session.commit()
    return {}
