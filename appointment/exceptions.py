from commons.exceptions import AppException


class Http400(Exception):
    http_code = 400


class ExceptionCodes:
    APPOINTMENT_ALREADY_EXISTS = 'APPOINTMENT001'
    APPOINTMENT_START_DATE = 'APPOINTMENT002'
    APPOINTMENT_END_DATE = 'APPOINTMENT003'


class AppointmentExistsException(AppException, Http400):
    def __init__(self, message='Appointment already exists'):
        super(AppointmentExistsException, self).__init__(message, ExceptionCodes.APPOINTMENT_ALREADY_EXISTS)


class AppointmentStartDateException(AppException, Http400):
    def __init__(self, message='Appointment cannot be before current date'):
        super(AppointmentStartDateException, self).__init__(message, ExceptionCodes.APPOINTMENT_START_DATE)


class AppointmentEndDateException(AppException, Http400):
    def __init__(self, message='Appointment can only be booked for next 7 days'):
        super(AppointmentEndDateException, self).__init__(message, ExceptionCodes.APPOINTMENT_END_DATE)