import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import UUID, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class BaseEntity(Base):  # type: ignore
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, onupdate=datetime.now, index=True
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
