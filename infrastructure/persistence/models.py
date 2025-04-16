import uuid

from sqlalchemy import Column, UUID, Boolean, String, Enum, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

from infrastructure.persistence.enums import RoleEnum

Entity = declarative_base()
metadata = Entity.metadata

class UserModel(Entity):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(LargeBinary, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    enabled = Column(Boolean, nullable=False, index=True, default=True)
