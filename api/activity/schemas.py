from datetime import datetime,date
from uuid import UUID
from typing import List

from api.schemas import PaginationSchema, InputSchema, BaseSchema, DisciplineMinimalSchema, ProfessorMinimalSchema


class ActivitySchema(BaseSchema):
    id: UUID
    title: str
    description: str
    date: date
    professor_id: UUID
    is_exam: bool
    professor: ProfessorMinimalSchema
    disciplines: List[DisciplineMinimalSchema]


class ActivityPaginationSchema(PaginationSchema):
    results: List[ActivitySchema]


class ActivityUpdateSchema(InputSchema):
    title: str
    description: str
    date: datetime
    disciplines_ids: List[UUID]


class ActivityCreateSchema(ActivityUpdateSchema):
    professor_id: UUID | None = None
