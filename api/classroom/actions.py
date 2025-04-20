from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from infrastructure.persistence.models import ClassroomModel, StudentModel


def sync_students(session: Session, classroom: ClassroomModel, students_ids: List[UUID]):
    students = session.query(StudentModel).where(StudentModel.id.in_(students_ids)).all()

    classroom.students = students
    session.flush()