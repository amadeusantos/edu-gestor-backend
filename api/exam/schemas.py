from typing import List
from uuid import UUID
from datetime import date, datetime

from api.schemas import BaseSchema, DisciplineMinimalSchema, PaginationSchema, InputSchema, ScoreMinimalSchema


class ExamSchema(BaseSchema):
    id: UUID
    title: str
    date: date
    is_finish: bool
    is_recovery: bool
    discipline_id: UUID
    discipline: DisciplineMinimalSchema
    scores: List[ScoreMinimalSchema]


class ExamPaginationSchema(PaginationSchema):
    results: List[ExamSchema]


class ExamUpdateSchema(InputSchema):
    title: str
    date: datetime
    is_finish: bool = False


class ExamCreateSchema(ExamUpdateSchema):
    is_recovery: bool = False
    discipline_id: UUID
