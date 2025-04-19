from api.exceptions import ServiceException


class StudentNotFoundException(ServiceException):
    def __init__(self):
        super().__init__(404, "Student not found")


class StudentCPFAlreadyExistsException(ServiceException):
    def __init__(self):
        super().__init__(409, "Student CPF already exists")

class StudentEnrollmentAlreadyExistsException(ServiceException):
    def __init__(self):
        super().__init__(409, "Student enrollment already exists")

class StudentCPFInvalidException(ValueError):
    def __init__(self):
        super().__init__("Student CPF invalid")

class StudentEmailInvalidException(ValueError):
    def __init__(self):
        super().__init__("Student email invalid")

class StudentPhoneInvalidException(ValueError):
    def __init__(self):
        super().__init__("Student phone invalid")