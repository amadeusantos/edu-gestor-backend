import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import UUID, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

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


class User(BaseEntity):  # type: ignore
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    enabled: Mapped[bool] = mapped_column(default=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id"), nullable=False
    )
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)


class RoleEnum(Enum):
    ADMIN = "ADMIN"
    COORDINATOR = "COORDINATOR"
    PROFESSOR = "PROFESSOR"
    STUDENT = "STUDENT"


class Profile(BaseEntity):  # type: ignore
    __tablename__ = "profiles"
    cpf: Mapped[str] = mapped_column(String(11), unique=True)
    enrollment: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    phone: Mapped[str] = mapped_column(String(11))
    fullname: Mapped[str] = mapped_column(String(64))
    sex: Mapped[Optional[bool]] = mapped_column(nullable=True)
    date_of_birth: Mapped[str] = mapped_column(DateTime)
    father_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    mother_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    responsible: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    role: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum))
    user: Mapped["User"] = relationship(back_populates="profile", uselist=False)
