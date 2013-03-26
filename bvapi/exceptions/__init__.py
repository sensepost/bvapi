class ApiException(Exception):
    """Base Exception class for all bvapi exceptions"""

class NotAuthorisedError(ApiException):
    """User was not authorized to perform the API call
    or access the specified resource"""

class NotFoundError(ApiException):
    """The specified resource was not found"""
