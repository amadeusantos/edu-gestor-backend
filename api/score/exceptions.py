from api.exceptions import ServiceException


class ScoreNotFoundException(ServiceException):
    def __init__(self):
        super().__init__(404, "Score not found")