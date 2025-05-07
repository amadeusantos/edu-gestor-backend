from uuid import UUID

from sqlalchemy.orm import Session

from infrastructure.persistence.models import UserModel


def actions_delete_student(session: Session, student_id: UUID):
    session.query(UserModel).where(UserModel.student_id == student_id).update({"enabled": False, "student_id": None})
    session.flush()