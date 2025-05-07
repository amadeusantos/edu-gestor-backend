from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query, Depends
from sqlalchemy.orm import Session

from api.authentication import Authorizations
from api.classroom.actions import sync_students
from api.classroom.exceptions import ClassroomNotFoundException
from api.classroom.schemas import ClassroomPaginationSchema, ClassroomSchema, ClassroomCreateSchema, \
    ClassroomUpdateSchema
from api.database import pagination
from api.schemas import UserPrincipal
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.enums import RoleEnum
from infrastructure.persistence.models import ClassroomModel

router = APIRouter(prefix="/classrooms", tags=["Classroom"])


def query_classrooms(session: Session):
    return session.query(ClassroomModel).where(ClassroomModel.deleted == False)


def query_first(session: Session, id: UUID):
    query = query_classrooms(session)
    classroom = query.where(ClassroomModel.id == id).first()

    if not classroom:
        raise ClassroomNotFoundException()

    return classroom


@router.get("")
def classrooms_pagination(
        search: str | None = Query(default=None),
        page: int = 1,
        size: int = 10,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> ClassroomPaginationSchema:
    query = query_classrooms(session)
    filters = []

    if search:
        filters.append(ClassroomModel.name.icontains(search))

    orders = [ClassroomModel.archived.desc()]

    return pagination(query, page, size, filters, orders)


@router.get("/{id}")
def get_classroom(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> ClassroomSchema:
    return query_first(session, id)


@router.post("")
def create_classroom(
        dto: ClassroomCreateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> ClassroomSchema:
    classroom = ClassroomModel(**dto.model_dump(exclude={"students_ids"}))
    session.add(classroom)
    session.flush()
    sync_students(session, classroom, dto.students_ids)
    session.commit()
    session.refresh(classroom)
    return classroom


@router.put("/{id}")
def update_classroom(
        id: UUID,
        dto: ClassroomUpdateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
) -> ClassroomSchema:
    classroom = query_first(session, id)
    session.query(ClassroomModel).where(ClassroomModel.id == classroom.id).update(dto.model_dump(exclude={"students_ids"}))
    session.flush()
    sync_students(session, classroom, dto.students_ids)
    session.commit()
    session.refresh(classroom)
    return classroom


@router.delete("/{id}", status_code=204)
def delete_classroom(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))
):
    classroom = query_first(session, id)
    session.query(ClassroomModel).where(ClassroomModel.id == classroom.id).update({"deleted": True})
    session.commit()
    return {}
