from typing import List
from uuid import UUID

from api.schemas import PaginationSchema, InputSchema, BaseSchema
from infrastructure.persistence.enums import RoleEnum

class UserCreateSchema(InputSchema):
    email: str
    password: str
    role: RoleEnum
    professor_id: UUID | None = None
    student_id: str | None = None

class UserUpdateSchema(InputSchema):
    email: str
    password: str | None = None
    role: RoleEnum
    professor_id: UUID | None = None
    student_id: str | None = None

class UserSchema(BaseSchema):
    id: UUID
    email: str
    role: RoleEnum
    enabled: bool
    professor_id: UUID | None = None
    student_id: UUID | None = None

class UserPaginationSchema(PaginationSchema):
    results: List[UserSchema]