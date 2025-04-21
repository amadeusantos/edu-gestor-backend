import uuid
from typing import List

from sqlalchemy import Column, UUID, Boolean, String, Enum, LargeBinary, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped

from infrastructure.persistence.enums import RoleEnum, SexEnum, ShiftEnum

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

    fullname = Column(String(60), nullable=False, index=True)
    cpf = Column(String(14), nullable=False, index=True)
    email = Column(String(64), index=True)
    phone = Column(String(15))
    date_of_birth = Column(Date, nullable=False)
    sex = Column(Enum(SexEnum), nullable=False)


class StudentModel(EntityBase, Entity):
    __tablename__ = "students"

    fullname = Column(String(64), nullable=False, index=True)
    cpf = Column(String(14), nullable=False, index=True)
    enrollment = Column(String(50), nullable=False, index=True)
    father_name = Column(String(64))
    mother_name = Column(String(64))
    responsible = Column(String(128), nullable=False)
    phone = Column(String(15))
    email = Column(String(64))
    date_of_birth = Column(Date, nullable=False)
    sex = Column(Enum(SexEnum), nullable=False)
    classroom_id = Column(ForeignKey('classrooms.id'))

    classroom: Mapped["ClassroomModel"] = relationship("ClassroomModel", back_populates="students")


class ClassroomModel(EntityBase, Entity):
    __tablename__ = "classrooms"

    name = Column(String(32), nullable=False, index=True)
    shift = Column(Enum(ShiftEnum), nullable=False, index=True)

    students: Mapped[List["StudentModel"]] = relationship("StudentModel", back_populates="classroom")


class DisciplineModel(EntityBase, Entity):
    __tablename__ = "disciplines"

    name = Column(String(64), nullable=False, index=True)
    professor_id = Column(ForeignKey('professors.id'))
    classroom_id = Column(ForeignKey("classrooms.id"))

    professor: Mapped["ProfessorModel"] = relationship("ProfessorModel")
    classroom: Mapped["ClassroomModel"] = relationship("ClassroomModel")


FrequencyStudentModel = Table(
    "frequencies_students",
    metadata,
    Column("frequency_id", ForeignKey("frequencies.id")),
    Column("student_id", ForeignKey("students.id"))
)


class FrequencyModel(EntityBase, Entity):
    __tablename__ = "frequencies"

    date = Column(Date, nullable=False, index=True)
    discipline_id: Mapped[str] = Column(ForeignKey("disciplines.id"), nullable=False)
    discipline: Mapped["DisciplineModel"] = relationship("DisciplineModel")
    presents: Mapped[List["StudentModel"]] = relationship("StudentModel", secondary="frequencies_students")

