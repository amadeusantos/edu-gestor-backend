from uuid import UUID

from sqlalchemy.orm import Session

from api.student.exceptions import StudentCPFAlreadyExistsException, StudentEnrollmentAlreadyExistsException
from api.student.schemas import StudentCreateSchema, StudentUpdateSchema
from infrastructure.persistence.models import StudentModel


def validate_create_student(session: Session, student_create: StudentCreateSchema):
    student = (
        session.query(StudentModel)
        .where(StudentModel.deleted == False, StudentModel.cpf == student_create.cpf)
        .first()
    )

    if student:
        raise StudentCPFAlreadyExistsException()

    student = (
        session.query(StudentModel)
        .where(StudentModel.deleted == False, StudentModel.enrollment == student_create.enrollment)
        .first()
    )

    if student:
        raise StudentEnrollmentAlreadyExistsException()

    return


def validate_update_student(session: Session, student_update: StudentUpdateSchema, id: UUID):
    student = (
        session.query(StudentModel)
        .where(StudentModel.deleted == False, StudentModel.cpf == student_update.cpf, StudentModel.id != id)
        .first()
    )

    if student:
        raise StudentCPFAlreadyExistsException()

    student = (
        session.query(StudentModel)
        .where(StudentModel.deleted == False, StudentModel.enrollment == student_update.enrollment,
               StudentModel.id != id)
        .first()
    )

    if student:
        raise StudentEnrollmentAlreadyExistsException()

    return
