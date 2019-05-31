# coding: utf-8

import logging

from tornado_skeleton.helpers.error_code import ErrorCode

_logger = logging.getLogger(__name__)


class ResponseErrors(object):
    @staticmethod
    def response_for(code, **kwargs):
        try:
            responses_per_code = {getattr(ErrorCode, name): getattr(ResponseErrors, name) for name in ErrorCode._member_names_}
        except AttributeError as e:
            _logger.error(e)
            return ResponseErrors.INTERNAL_SERVER_ERROR
        return dict(responses_per_code[code],
                    detail=responses_per_code[code]['detail'].format(**kwargs))

    USER_NOT_FOUND = {
        'status': 404,
        'code': str(ErrorCode.USER_NOT_FOUND),
        'title': 'User Not Found',
        'detail': 'The user {user} was not found.'
    }

    USER_ALREADY_EXISTS = {
        'status': 409,
        'code': str(ErrorCode.USER_ALREADY_EXISTS),
        'title': 'User Already Exists',
        'detail': 'The user {user} already exists, cannot create one.'
    }

    MISSING_BODY = {
        'status': 422,
        'code': str(ErrorCode.MISSING_BODY),
        'title': 'Missing Body',
        'detail': 'The body is missing but required for this request.'
    }

    MISSING_PARAMETER = {
        'status': 422,
        'code': str(ErrorCode.MISSING_PARAMETER),
        'title': 'Missing Parameter',
        'detail': 'The parameter {parameter} is missing.'
    }

    WRONG_PARAMETER_TYPE = {
        'status': 422,
        'code': str(ErrorCode.WRONG_PARAMETER_TYPE),
        'title': 'Wrong Parameter Type',
        'detail': 'The parameter {parameter} must be a {type}.'
    }

    METHOD_NOT_ALLOWED = {
        'status': 405,
        'code': str(ErrorCode.METHOD_NOT_ALLOWED),
        'title': 'Method Not Allowed',
        'detail': 'The method {method} is not allowed for this request.'
    }

    CONTENT_TYPE_HEADER_ERROR = {
        'status': 400,
        'code': str(ErrorCode.CONTENT_TYPE_HEADER_ERROR),
        'title': 'Content-Type Header Error',
        'detail': 'The Content-Type header is missing or invalid, with Gandalf only accepting \'Content-Type: application/json*\' headers.'
    }

    INTERNAL_SERVER_ERROR = {
        'status': 500,
        'code': str(ErrorCode.INTERNAL_SERVER_ERROR),
        'title': 'Internal Server Error',
        'detail': 'We are working to resolve this issue. If the error persists, please contact {contact}.'
    }
