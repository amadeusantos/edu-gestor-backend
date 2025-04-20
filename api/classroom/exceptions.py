from api.exceptions import ServiceException


class ClassroomNotFoundException(ServiceException):
    def __init__(self):
        super().__init__(404, "Classroom not found")