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


class ProfileResponse(BaseModel):
    id: str
    created_at: str
    updated_at: Optional[str]
    cpf: str
    enrollment: Optional[str]
    phone: str
    fullname: str
    sex: Optional[bool]
    date_of_birth: str
    father_name: Optional[str]
    mother_name: Optional[str]
    responsible: Optional[str]
    role: str
    user_id: Optional[str]

    @classmethod
    def from_row(cls, row: User) -> "ProfileResponse":
        return cls(
            id=str(row.id),
            created_at=row.created_at.isoformat(),
            updated_at=row.updated_at.isoformat() if row.updated_at else None,
            cpf=row.cpf,
            enrollment=row.enrollment,
            phone=row.phone,
            fullname=row.fullname,
            sex=row.sex,
            date_of_birth=row.date_of_birth.isoformat(),
            father_name=row.father_name,
            mother_name=row.mother_name,
            responsible=row.responsible,
            role=row.role.value,
            user_id=str(row.user.id) if row.user else None,
        )
