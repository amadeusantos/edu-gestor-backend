import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import BinaryExpression, ColumnElement
from core.infrastructure.database.tables import Profile, RoleEnum, User


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    profile_id: str

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        pattern = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        if not pattern.match(password):
            raise ValueError(
                "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        return password

    def to_row(self) -> User:
        return User(
            email=str(self.email), password=self.password, profile_id=self.profile_id
        )


class ProfileRequest(BaseModel):
    cpf: str
    enrollment: Optional[str] = None
    phone: str
    fullname: str
    sex: Optional[bool] = None
    date_of_birth: str
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    responsible: Optional[str] = None
    role: RoleEnum

    @field_validator("cpf")
    def validate_cpf(cls, cpf: str) -> str:
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("Invalid CPF format. Must be 11 digits.")
        return cpf

    @field_validator("phone")
    def validate_phone(cls, phone: str) -> str:
        if len(phone) != 11 or not phone.isdigit():
            raise ValueError("Invalid phone format. Must be 11 digits.")
        return phone

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, date_of_birth: str) -> str:
        try:
            datetime.strptime(date_of_birth, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        return date_of_birth

    def to_row(self) -> Profile:
        return Profile(
            cpf=self.cpf,
            enrollment=self.enrollment,
            phone=self.phone,
            fullname=self.fullname,
            sex=self.sex,
            date_of_birth=datetime.strptime(self.date_of_birth, "%Y-%m-%d"),
            father_name=self.father_name,
            mother_name=self.mother_name,
            responsible=self.responsible,
            role=self.role,
        )


class ProfileFiltersRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
    cpf: Optional[str] = Field(default=None, max_length=11)
    fullname: Optional[str] = Field(default=None, max_length=64)
    role: Optional[RoleEnum] = Field(default=None)

    def to_query_filters(self) -> list:
        filters: list[BinaryExpression[bool] | ColumnElement[bool] | None] = []
        if self.cpf:
            filters.append(Profile.cpf.ilike(f"%{self.cpf}%"))
        if self.fullname:
            filters.append(Profile.fullname.ilike(f"%{self.fullname}%"))
        if self.role:
            filters.append(Profile.role == self.role)

        return filters
