from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from api.activity.actions import sync_disciplines
from api.activity.exceptions import ActivityNotFoundException
from api.activity.schemas import ActivitySchema, ActivityCreateSchema, ActivityUpdateSchema
from api.activity.validations import validate_create_activities
from api.authentication import Authorizations
from api.schemas import UserPrincipal
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.enums import RoleEnum
from infrastructure.persistence.models import ActivityModel, DisciplineModel, StudentModel, ClassroomModel

router = APIRouter(prefix="/activities", tags=["Activity"])


def query_activities(session: Session, user_principal: UserPrincipal):
    filters = []

    if not (user_principal.role == RoleEnum.COORDINATOR.value or user_principal.role == RoleEnum.ADMIN.value):
        if user_principal.role == RoleEnum.PROFESSOR.value:
            classrooms = session.query(ClassroomModel.id).where(
                ClassroomModel.disciplines.any(DisciplineModel.professor_id == user_principal.professor_id)).all()
        else:
            classrooms = session.query(ClassroomModel.id).where(
                ClassroomModel.students.any(StudentModel.id == user_principal.student_id)).all()

        classrooms_ids = [c.id for c in classrooms]
        filters.append(ActivityModel.disciplines.any(DisciplineModel.classroom_id.in_(classrooms_ids)))

    return session.query(ActivityModel).where(ActivityModel.deleted == False, *filters)


def query_first(session: Session, id: UUID, user_principal: UserPrincipal):
    query = query_activities(session, user_principal)
    activity = query.where(ActivityModel.id == id).first()
    if not activity:
        raise ActivityNotFoundException()
    return activity


@router.get("")
def activity_list(
        gte_date: datetime,
        lte_date: datetime,
        classroom_id: UUID | None = Query(default=None),
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations(
                [RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR, RoleEnum.STUDENT, RoleEnum.RESPONSIBLE]))
) -> List[ActivitySchema]:
    query = query_activities(session, user_principal)
    filters = [ActivityModel.date >= gte_date.date(), ActivityModel.date <= lte_date.date()]

    if classroom_id:
        filters.append(ActivityModel.disciplines.contains(DisciplineModel.classroom_id == classroom_id))

    orders = [ActivityModel.date]

    return query.where(*filters).order_by(*orders).all()


@router.get("/{id}")
def get_activity(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations(
                [RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR, RoleEnum.STUDENT, RoleEnum.RESPONSIBLE]))
) -> ActivitySchema:
    return query_first(session, id, user_principal)


@router.post("")
def create_activity(
        dto: ActivityCreateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> ActivitySchema:
    dto = validate_create_activities(dto, user_principal)
    activity = ActivityModel(**dto.model_dump(exclude={"disciplines_ids"}))
    session.add(activity)
    session.flush()
    sync_disciplines(session, activity, dto.disciplines_ids)
    session.commit()
    session.refresh(activity)
    return activity


@router.put("/{id}")
def update_activity(
        id: UUID,
        dto: ActivityUpdateSchema,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
) -> ActivitySchema:
    activity = query_first(session, id, user_principal)
    session.query(ActivityModel).where(ActivityModel.id == activity.id).update(
        dto.model_dump(exclude={"disciplines_ids"}))
    session.flush()
    sync_disciplines(session, activity, dto.disciplines_ids)
    session.commit()
    session.refresh(activity)
    return activity


@router.delete("/{id}", status_code=204)
def delete_activity(
        id: UUID,
        session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR]))
):
    activity = query_first(session, id, user_principal)
    session.query(ActivityModel).where(ActivityModel.id == activity.id).update({"deleted": True})
    session.commit()
    return {}
