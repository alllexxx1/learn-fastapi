from fastapi import HTTPException, status


class BaseBookingException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BaseBookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User with such email already exists'


class IncorrectCredentialsException(BaseBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Wrong credentials'


class NoTokenException(BaseBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User is not authorized. Token hasn't been passed"


class IncorrectTokenFormatException(BaseBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect token format'


class ExpiredTokenException(BaseBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token expired'


class InsufficientPayloadDataException(BaseBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'User_id is missed in token payload'


class NoSuchUserException(BaseBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User with given ID wasn't found in DB"


class RoomCannotBeBookedException(BaseBookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'All rooms are booked'


class BookingCannotBeDeletedException(BaseBookingException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = 'You are not allowed to delete this resource'


class DateMessException(BaseBookingException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = 'The check-in date cannot be later than the check-out date'


class TooLongBookingPeriodException(BaseBookingException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = 'The maximum booking period is 31 days'


class NoRightsException(BaseBookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Get out of here!'
