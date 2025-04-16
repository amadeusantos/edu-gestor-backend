from enum import Enum

class RoleEnum(Enum):
    PROFESSOR ='PROFESSOR'
    COORDINATOR = 'COORDINATOR'
    ADMIN ='ADMIN'
    STUDENT ='STUDENT'
    RESPONSIBLE ='RESPONSIBLE'

class SexEnum(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"