from api.exceptions import ServiceException


class UserNotFoundException(ServiceException):
    def __init__(self):
        super().__init__(404, "User not found")

class UserEmailAlreadyExistsException(ServiceException):
    def __init__(self):
        super().__init__(409, "User email already exists")