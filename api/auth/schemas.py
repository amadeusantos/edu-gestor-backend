from uuid import UUID

from api.schemas import BaseSchema, InputSchema


class AuthenticationSchema(InputSchema):
    email: str
    password: str

class TokenSchema(BaseSchema):
    token: str

class AuthenticatedSchema(BaseSchema):
    id: UUID
    role: str