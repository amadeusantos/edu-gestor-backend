from typing import List
from uuid import UUID

from api.schemas import PaginationSchema, BaseSchema, InputSchema, ClassroomMinimalSchema, ProfessorMinimalSchema


class DisciplineSchema(BaseSchema):
    id: UUID
    name: str
    classroom_id: UUID
    classroom: ClassroomMinimalSchema
    professor_id: UUID | None = None
    professor: ProfessorMinimalSchema | None = None


class DisciplinePaginationSchema(PaginationSchema):
    results: List[DisciplineSchema]


class DisciplineUpdateSchema(InputSchema):
    name: str
    professor_id: UUID | None = None


class DisciplineCreateSchema(DisciplineUpdateSchema):
    classroom_id: UUID
