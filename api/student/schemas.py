from decimal import Decimal
from uuid import UUID
from datetime import date, datetime
from typing import List

from pydantic import field_validator

from api.schemas import PaginationSchema, BaseSchema, InputSchema, ClassroomMinimalSchema
from api.student.exceptions import StudentCPFInvalidException, StudentEmailInvalidException, \
    StudentPhoneInvalidException
from api.utils import validate_cpf, format_cpf, validate_email, validate_phone, format_phone
from infrastructure.persistence.enums import SexEnum


class StudentSchema(BaseSchema):
    id: UUID
    fullname: str
    cpf: str
    enrollment: str
    father_name: str | None = None
    mother_name: str | None = None
    responsible: str
    phone: str
    email: str | None = None
    date_of_birth: date
    sex: SexEnum
    classroom_id: UUID | None = None
    classroom: ClassroomMinimalSchema | None = None


class StudentPaginationSchema(PaginationSchema):
    results: List[StudentSchema]


class StudentInfoSchema(BaseSchema):
    discipline_id: UUID
    discipline_name: str
    professor_name: str
    faults: int
    classes: int
    average_grade: float


class StudentInfoPaginationSchema(PaginationSchema):
    results: List[StudentInfoSchema]


class StudentUpdateSchema(InputSchema):
    fullname: str
    father_name: str | None = None
    mother_name: str | None = None
    responsible: str
    phone: str
    email: str | None = None
    cpf: str
    enrollment: str
    date_of_birth: datetime
    sex: SexEnum

    @field_validator("email")
    def validator_email(cls, value):
        if value and not validate_email(str(value)):
            raise StudentEmailInvalidException()
        return value

    @field_validator("cpf")
    def validator_cpf(cls, value):
        if not validate_cpf(str(value)):
            raise StudentCPFInvalidException()
        return format_cpf(str(value))

    @field_validator("phone")
    def validator_phone(cls, value):
        if not value:
            return None
        if not validate_phone(str(value)):
            raise StudentPhoneInvalidException()
        return format_phone(str(value))


class StudentCreateSchema(StudentUpdateSchema):
    pass
