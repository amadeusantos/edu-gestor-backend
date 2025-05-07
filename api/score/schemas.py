from decimal import Decimal
from uuid import UUID

from api.schemas import BaseSchema, InputSchema


class ScoreSchema(BaseSchema):
    id: UUID
    value: Decimal
    is_absent: bool
    fullname: str

class ScoreUpdateSchema(InputSchema):
    value: Decimal
    is_absent: bool