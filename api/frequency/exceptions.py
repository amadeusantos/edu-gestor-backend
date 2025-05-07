from api.exceptions import ServiceException


class FrequencyNotFoundException(ServiceException):
    def __init__(self):
        super().__init__(404, "Frequency not found")