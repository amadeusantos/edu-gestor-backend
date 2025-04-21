from typing import List
from uuid import UUID
from datetime import date, datetime

from api.schemas import BaseSchema, DisciplineMinimalSchema, StudentMinimalSchema, PaginationSchema, InputSchema
from api.student.schemas import StudentUpdateSchema


class FrequencySchema(BaseSchema):
    id: UUID
    date: date
    discipline_id: UUID
    discipline: DisciplineMinimalSchema
    presents: List[StudentMinimalSchema]


class FrequencyPaginationSchema(PaginationSchema):
    results: List[FrequencySchema]

class FrequencyUpdateSchema(InputSchema):
    presents_ids: List[UUID]


class FrequencyCreateSchema(FrequencyUpdateSchema):
    date: datetime
    discipline_id: UUID