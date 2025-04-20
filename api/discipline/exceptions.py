from api.exceptions import ServiceException


class DisciplineNotFoundException(ServiceException):
    def __init__(self):
        super().__init__(404, "Discipline not found")