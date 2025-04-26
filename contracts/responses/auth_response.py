from pydantic import BaseModel
from core.infrastructure.database.tables import User
from typing import Optional


class AuthenticationResponse(BaseModel):
    user_id: str
    access_token: str
    exp_time: float

    @classmethod
    def from_row(
        cls, row: User, access_token: str, exp_time: float
    ) -> "AuthenticationResponse":
        return cls(
            user_id=str(row.id),
            access_token=access_token,
            exp_time=exp_time,
        )


class CurrentUserResponse(BaseModel):
    user_id: str
    role: Optional[str]

    @classmethod
    def from_row(cls, row: User) -> "CurrentUserResponse":
        return cls(
            user_id=str(row.id),
            role=row.profile.role.value if row.profile.role else None,
        )
