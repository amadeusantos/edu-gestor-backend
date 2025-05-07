from api.exceptions import ServiceException


class ProfessorNotFoundException(ServiceException):
    def __init__(self):
        super().__init__(404, "Professor not found", 300)

class ProfessorCPFAlreadyExistsException(ServiceException):
    def __init__(self):
        super().__init__(409, "Professor CPF already exists", 301)

class ProfessorCPFInvalidException(ValueError):
    def __init__(self):
        super().__init__("Professor CPF invalid")

class ProfessorEmailInvalidException(ValueError):
    def __init__(self):
        super().__init__("Professor email invalid")

class ProfessorPhoneInvalidException(ValueError):
    def __init__(self):
        super().__init__("Professor phone invalid")