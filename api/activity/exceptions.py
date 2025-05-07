from api.exceptions import ServiceException


class ActivityNotFoundException(ServiceException):
    def __init__(self):
        super().__init__(404, "Coordinator not found")

class ActivityProfessorIdException(ServiceException):
    def __init__(self):
        super().__init__(409, "Activity without teacher")