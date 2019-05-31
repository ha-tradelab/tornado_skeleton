"""
Read this:
https://fr.wikipedia.org/wiki/Liste_des_codes_HTTP
"""
from enum import Enum


class ErrorCode(Enum):
    """
    Gandalf error codes across all software.
    """
    USER_NOT_FOUND = 1200  # Kasserine, TN
    USER_ALREADY_EXISTS = 1300

    MISSING_BODY = 75017  # Paris 17th, FR
    MISSING_PARAMETER = 75018  # Paris 18th, FR
    WRONG_PARAMETER_TYPE = 75019  # Paris 19th, FR
    METHOD_NOT_ALLOWED = 75020  # Paris 20th, FR
    CONTENT_TYPE_HEADER_ERROR = 76000  # Rouen, FR

    INTERNAL_SERVER_ERROR = 92260  # Fontenay-aux-Roses, FR

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)
