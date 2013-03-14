class ApiException(Exception):
    pass

class NotAuthorisedError(ApiException):
    pass

class NotFoundError(ApiException):
    pass
