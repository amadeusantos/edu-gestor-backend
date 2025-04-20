from typing import List
from uuid import UUID

from api.schemas import PaginationSchema, StudentMinimalSchema
from api.schemas import BaseSchema, InputSchema
from infrastructure.persistence.enums import ShiftEnum


class ClassroomSchema(BaseSchema):
    id: UUID
    name: str
    shift: ShiftEnum
    students: List[StudentMinimalSchema] = []

class ClassroomPaginationSchema(PaginationSchema):
    results: List[ClassroomSchema]

class ClassroomUpdateSchema(InputSchema):
    name: str
    shift: ShiftEnum
    students_ids: List[UUID] = []

class ClassroomCreateSchema(ClassroomUpdateSchema):
    pass