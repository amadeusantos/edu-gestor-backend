from api.exceptions import ServiceException


class ExamNotFoundException(ServiceException):
    def __init__(self):
        super().__init__(404, "Exam not found")