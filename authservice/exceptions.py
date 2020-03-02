from commons.exceptions import AppException


class Http400(Exception):
    http_code = 400


class ExceptionCodes:
    EMAIL_ALREADY_EXISTS = 'AUTH001'


class EmailAlreadyRegisteredException(AppException, Http400):
    def __init__(self, message='Email already exists'):
        super(EmailAlreadyRegisteredException, self).__init__(message, ExceptionCodes.EMAIL_ALREADY_EXISTS)
