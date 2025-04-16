class ServiceException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

class NotAuthenticated(ServiceException):
    def __init__(self):
        super().__init__(401, "User or password is incorrect")

class TokenInvalidException(ServiceException):
    def __init__(self):
        super().__init__(401, "token invalid")

class ForbiddenException(ServiceException):
    def __init__(self):
        super().__init__(401, "user not authorized")