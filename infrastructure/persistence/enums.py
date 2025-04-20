from enum import Enum

class RoleEnum(Enum):
    PROFESSOR ='PROFESSOR'
    COORDINATOR = 'COORDINATOR'
    ADMIN ='ADMIN'
    STUDENT ='STUDENT'
    RESPONSIBLE ='RESPONSIBLE'

class ShiftEnum(Enum):
    MORNING = 'MORNING'
    AFTERNOON = 'AFTERNOON'
    NIGHT = 'NIGHT'

class SexEnum(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"