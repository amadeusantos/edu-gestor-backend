from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from infrastructure.persistence.models import ActivityModel, DisciplineModel


def sync_disciplines(session: Session, activity: ActivityModel, disciplines_ids: List[UUID]):
    disciplines = session.query(DisciplineModel).where(DisciplineModel.id.in_(disciplines_ids)).all()

    activity.disciplines = disciplines
    session.flush()
