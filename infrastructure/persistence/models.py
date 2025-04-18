import uuid

from sqlalchemy import Column, UUID, Boolean, String, Enum, LargeBinary, Date
from sqlalchemy.ext.declarative import declarative_base

from infrastructure.persistence.enums import RoleEnum, SexEnum

Entity = declarative_base()
metadata = Entity.metadata


class EntityBase:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    archived = Column(Boolean, nullable=False, index=True, default=False)
    deleted = Column(Boolean, nullable=False, index=True, default=False)


class UserModel(Entity):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(LargeBinary, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    enabled = Column(Boolean, nullable=False, index=True, default=True)


class ProfessorModel(EntityBase, Entity):
    __tablename__ = "professors"

    fullname = Column(String, nullable=False, index=True)
    cpf = Column(String(14), nullable=False, index=True)
    email = Column(String(64), index=True)
    phone = Column(String(15))
    date_of_birth = Column(Date, nullable=False)
    sex = Column(Enum(SexEnum), nullable=False)
