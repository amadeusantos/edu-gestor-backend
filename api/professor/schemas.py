from typing import List
from uuid import UUID
from datetime import date, datetime

from pydantic import field_validator

from api.professor.exceptions import ProfessorEmailInvalidException, ProfessorCPFInvalidException, \
    ProfessorPhoneInvalidException
from api.schemas import PaginationSchema, BaseSchema, InputSchema
from api.utils import validate_email, validate_cpf, format_cpf, validate_phone, format_phone
from infrastructure.persistence.enums import SexEnum


class ProfessorSchema(BaseSchema):
    id: UUID
    fullname: str
    cpf: str
    email: str | None
    phone: str | None
    date_of_birth: date
    sex: SexEnum
    disciplines: List = []

class ProfessorPaginationSchema(PaginationSchema):
    results: List[ProfessorSchema]

class ProfessorUpdateSchema(InputSchema):
    fullname: str
    email: str | None
    phone: str | None
    cpf: str
    date_of_birth: datetime
    sex: SexEnum

    @field_validator("email")
    def validator_email(cls, value):
        if value and not validate_email(str(value)):
            raise ProfessorEmailInvalidException()
        return value

    @field_validator("phone")
    def validator_phone(cls, value):
        if not value:
            return None
        if not validate_phone(str(value)):
            raise ProfessorPhoneInvalidException()
        return format_phone(str(value))

    @field_validator("cpf")
    def validator_cpf(cls, value):
        if not validate_cpf(str(value)):
            raise ProfessorCPFInvalidException()
        return format_cpf(str(value))

class ProfessorCreateSchema(ProfessorUpdateSchema):
    pass
