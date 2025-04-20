from pydantic import BaseModel
from core.infrastructure.database.tables import User


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
