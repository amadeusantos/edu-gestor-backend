from typing import Optional
from pydantic import BaseModel
from core.infrastructure.database.tables import User


class UserResponse(BaseModel):
    id: str
    created_at: str
    updated_at: Optional[str]
    email: str
    role: str
    enabled: bool

    @classmethod
    def from_row(cls, row: User) -> "UserResponse":
        return cls(
            id=str(row.id),
            created_at=row.created_at.isoformat(),
            updated_at=row.updated_at.isoformat() if row.updated_at else None,
            email=row.email,
            role=row.role.value,
            enabled=row.enabled,
        )
