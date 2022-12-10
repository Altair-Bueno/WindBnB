class AlreadyBookedError(Exception):
    error_code = 'ALREADY_BOOKED'

class UpdateBookingError(Exception):
    error_code = 'UPDATE_ERROR'


class NotFoundError(Exception):
    error_code = 'NOT_FOUND'
