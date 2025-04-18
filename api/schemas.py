from uuid import UUID
from typing import List

from pydantic import BaseModel, ConfigDict

from infrastructure.persistence.enums import RoleEnum


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
