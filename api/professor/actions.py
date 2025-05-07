from uuid import UUID

from sqlalchemy.orm import Session

from infrastructure.persistence.models import UserModel, DisciplineModel


def actions_delete_professor(session: Session, professor_id: UUID):
    session.query(UserModel).where(UserModel.professor_id == professor_id).update({"enabled": False, "professor_id": None})
    session.query(DisciplineModel).where(DisciplineModel.professor_id == professor_id).update({"professor_id": None})
    session.flush()