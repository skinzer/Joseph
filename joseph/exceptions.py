class JosephException(Exception):
    pass


class ConfigException(JosephException):
    pass


class InvalidState(JosephException):
    pass