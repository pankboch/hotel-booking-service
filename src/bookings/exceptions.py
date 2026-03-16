class BookingError(Exception):
    """Базовая ошибка бронирования."""

    pass


class RoomNotFoundError(BookingError):
    pass


class InvalidDateRangeError(BookingError):
    pass


class BookingOverlapError(BookingError):
    pass


class BookingNotFoundError(BookingError):
    pass
