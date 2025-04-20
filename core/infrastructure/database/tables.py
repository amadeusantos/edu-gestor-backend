import uuid
from enum import Enum
from typing import Optional
from sqlalchemy import UUID, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class BaseEntity(Base):  # type: ignore
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[DateTime] = mapped_column(default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )


class RoleEnum(Enum):
    PROFESSOR = "PROFESSOR"
    COORDINATOR = "COORDINATOR"
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    RESPONSIBLE = "RESPONSIBLE"


class User(BaseEntity):  # type: ignore
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    role: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum))
    enabled: Mapped[bool] = mapped_column(default=True)


class UniversityMember(BaseEntity):  # type: ignore
    __tablename__ = "university_members"
    cpf: Mapped[str] = mapped_column(String(14), unique=True)
    enrollment: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    email: Mapped[str] = mapped_column(String(64), index=True)
    phone: Mapped[str] = mapped_column(String(15))
    fullname: Mapped[str] = mapped_column(String(64))
    sex: Mapped[Optional[bool]] = mapped_column(nullable=True)
    date_of_birth: Mapped[str] = mapped_column(DateTime)
    father_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    mother_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    responsible: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
