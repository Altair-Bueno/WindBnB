class AlreadyBookedError(Exception):
    error_code = 'ALREADY_BOOKED'


class NotFoundError(Exception):
    error_code = 'NOT_FOUND'
