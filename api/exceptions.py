class ServiceException(Exception):
    def __init__(self, status_code: int, message: str, error_code: int = 0):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class NotAuthenticated(ServiceException):
    def __init__(self):
        super().__init__(401, "User or password is incorrect", 1)

class TokenInvalidException(ServiceException):
    def __init__(self):
        super().__init__(401, "token invalid", 2)

class ForbiddenException(ServiceException):
    def __init__(self):
        super().__init__(403, "user not authorized", 3)