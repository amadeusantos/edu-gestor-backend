from uuid import UUID

from sqlalchemy.orm import Session

from api.professor.exceptions import ProfessorCPFAlreadyExistsException
from api.professor.schemas import ProfessorCreateSchema, ProfessorUpdateSchema
from infrastructure.persistence.models import ProfessorModel


def validate_create_professor(session: Session, professor_create: ProfessorCreateSchema):
    professor = (
        session.query(ProfessorModel)
        .where(ProfessorModel.deleted == False, ProfessorModel.cpf == professor_create.cpf)
        .first()
    )

    if professor:
        raise ProfessorCPFAlreadyExistsException()


def validate_update_professor(session: Session, professor_update: ProfessorUpdateSchema, professor_id: UUID):
    professor = (
        session.query(ProfessorModel)
        .where(ProfessorModel.deleted == False, ProfessorModel.cpf == professor_update.cpf,
               ProfessorModel.id != professor_id)
        .first()
    )

    if professor:
        raise ProfessorCPFAlreadyExistsException()
