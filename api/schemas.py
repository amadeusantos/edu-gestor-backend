from uuid import UUID
from typing import List

from pydantic import BaseModel, ConfigDict

from infrastructure.persistence.enums import RoleEnum, SexEnum, ShiftEnum


class InputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseSchema(BaseModel):
    model_config = ConfigDict(use_enum_values=True, str_strip_whitespace=True)


class PaginationSchema(BaseSchema):
    total_items: int
    total_pages: int
    page: int
    size: int
    results: List[BaseSchema]


class UserPrincipal(BaseSchema):
    id: UUID
    role: RoleEnum
    student_id: UUID | None = None
    professor_id: UUID | None = None


class StudentMinimalSchema(BaseSchema):
    id: UUID
    fullname: str
    responsible: str
    sex: SexEnum
    classroom_id: UUID | None = None


class ClassroomMinimalSchema(BaseSchema):
    id: UUID
    name: str
    shift: ShiftEnum

class ProfessorMinimalSchema(BaseSchema):
    id: UUID
    fullname: str
    sex: SexEnum

class DisciplineMinimalSchema(BaseSchema):
    id: UUID
    name: str
    classroom_id: UUID
    professor_id: UUID | None = None