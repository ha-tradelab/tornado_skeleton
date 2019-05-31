# coding: utf-8

import logging

try:
    import ujson as json
except ImportError:
    import json
from tornado.web import RequestHandler
from tradelab.collections.smart_dict import SmartDict

from tornado_skeleton.helpers.error_code import ErrorCode
from tornado_skeleton.api.response_errors import ResponseErrors


CONTENT_TYPE = 'application/json'

ALLOWED_ORIGIN = '*'

ALLOWED_HEADERS = (
    'Authorization',
    'X-Requested-With',
    'X-Access-Token',
    'X-Service-Token',
    'Content-Type'
)

ALLOWED_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

AUTHORIZATION_HEADER = 'Authorization'


class BaseHandler(RequestHandler):
    """
    Base handler inheriting from tornado.web.RequestHandler.
    Provide many helpers for handlers across the Gandalf API
    from requests initialization to response production
    and error management.
    This class also inherits from tornado_sqlalchemy.SessionMixin
    to provide SqlAlchemy session helpers such as a
    contextual session creation.
    """

    def __init__(self, application, request, **kwargs):
        """
        Initialize the BaseHandler object with the initializers parameters.
        These parameters include metadata such as env and version,
        logging operators and HTTP access control values.

        :param application: The application used to hold handlers.
        :type application: gandalf.api.WebApplication
        :param request: The request received by the API.
        :type request: request
        :param kwargs: Keyword arguments containing initializing parameters.
        :type kwargs: dict
        """
        kwargs = SmartDict(**kwargs, raise_none=False)
        self.env = kwargs.get('env', '')
        self.version = kwargs.get('version', None)

        # Why don't we use the default parameter of kwargs.get(value, default) here?
        # Because if we do kwargs.get('logger', logging_context.get_logger(__name__)),
        # the method logging_context.get_logger(__name__) is executed EVEN IF kwargs['logger']
        # exists; the method is executed, but the result is not returned to self.logger
        # The issue is that by executing the method logging_context.get_logger(__name__),
        # the current logger for the module seems to be set, and future logs in this module
        # won't be displayed with the 'api' logger but the 'job_handler' logger, which doesn't
        # have any specifications in logging.yaml.
        # The following code ensures that logging_context.get_logger(__name__) is executed
        # ONLY IF kwargs doesn't contain a 'logger' keyword-argument.
        self.logger = kwargs.get('logger')
        if not self.logger:
            self.logger = logging.getLogger(__name__)

        self.allowed_origin = kwargs.get('access_control:allowed_origin', ALLOWED_ORIGIN)
        self.allowed_headers = kwargs.get('access_control:allowed_headers', ALLOWED_HEADERS)
        self.allowed_methods = kwargs.get('access_control:allowed_methods', ALLOWED_METHODS)

        self.initialize(**kwargs.get())
        super().__init__(application, request, **kwargs.get())

    def initialize(self, **kwargs):
        """
        Empty method to override in inheriting classes.
        E.g. can be used to set specific headers for each Handler.
        """
        pass

    def set_default_headers(self):
        """
        Set default headers for every API endpoint inheriting BaseHandler.
        Override RequestHandler.set_default_headers().
        """
        self.set_header('Content-Type', CONTENT_TYPE)
        self.set_header('Access-Control-Allow-Origin', self.allowed_origin)
        self.set_header('Access-Control-Allow-Headers', ','.join(self.allowed_headers))
        self.set_header('Access-Control-Allow-Methods', ','.join(self.allowed_methods))

    def post(self, *args, **kwargs):
        """
        POST methods are used to create new documents for the endpoints resources.
        Successful POST methods return a 201 Created HTTP status.

        If not implemented in the handlers inheriting from
        gandalf.api.handlers.BaseHandler, the method is not allowed.
        """
        self.method_not_allowed_error('POST')

    def get(self, *args, **kwargs):
        """
        GET methods are used to read or fetch resources.
        Successful GET methods return a 200 OK HTTP status.
        Unsuccessful GET methods generally return 404 Not Found or 400 Bad Request HTTP status.

        If not implemented in the handlers inheriting from
        gandalf.api.handlers.BaseHandler, the method is not allowed.
        """
        self.method_not_allowed_error('GET')

    def put(self, *args, **kwargs):
        """
        PUT methods are used to replace resources.
        Successful PUT methods return a 200 OK or a 204 No Content HTTP status.
        Unsuccessful PUT methods generally return a 404 Not Found HTTP status.

        If not implemented in the handlers inheriting from
        gandalf.api.handlers.BaseHandler, the method is not allowed.
        """
        self.method_not_allowed_error('PUT')

    def patch(self, *args, **kwargs):
        """
        PATCH methods are used to update resources.
        Successful PATCH methods return a 200 OK or a 204 No Content HTTP status.
        Unsuccessful PATCH methods generally return a 404 Not Found HTTP status.

        If not implemented in the handlers inheriting from
        gandalf.api.handlers.BaseHandler, the method is not allowed.
        """
        self.method_not_allowed_error('PATCH')

    def delete(self, *args, **kwargs):
        """
        DELETE methods are used to delete resources.
        Successful DELETE methods generally return a 200 OK or a 204 No Content HTTP status.
        Unsuccessful DELETE methods generally return a 404 Not Found HTTP status.

        If not implemented in the handlers inheriting from
        gandalf.api.handlers.BaseHandler, the method is not allowed.
        """
        self.method_not_allowed_error('DELETE')

    def options(self, *args, **kwargs):
        """
        Override RequestHandler.options() to provide a base endpoint for OPTIONS requests.
        Primarily used for CORS policy checking OPTIONS on the server.
        """
        self.set_status(204)
        self.finish()

    def send_response(self, data, status=200):
        """
        Send a response to the client with a RequestHandler.write operation.

        :param data: The data to send as a response.
        :type data: bytes, unicode, dict
        :param status: A HTTP status code for the response.
                       By default 200
        :type status: int
        """
        self.set_status(status)
        if not data:
            return self.finish()
        try:
            self.write(json.dumps(data))
        except (RuntimeError, TypeError) as e:
            self.logger.error(e)
            self.internal_server_error()

    def write_error(self, status_code, **kwargs):
        """
        Transform an error to a valid response and send it to the client.

        :param status_code: The HTTP status code for the response.
        :type status_code: int
        :param kwargs: Keyword arguments containing a `data` argument
                       holding the error response to send.
        :type kwargs: dict
        """
        data = kwargs.get('data')
        if data:
            self.logger.error('%s - %s - %s',
                              data.get('status', 'NO_STATUS'),
                              data.get('code', 'NO_CODE'),
                              data.get('title', 'NO_TITLE'))
        self.send_response(data, status_code)

    def produce_error(self, code, **kwargs):
        """
        Produce and send an error from an ErrorCode enum.
        Create a gandalf.api.response_errors.ResponseError
        from a gandalf.helpers.error_code.ErrorCode enum value.
        Use the overriden BaseHandler.send_error() method to
        create a response from the gandalf.api.response_errors.ResponseError.

        :param code: The ErrorCode used to produce a ResponseError and send a response.
        :type code: gandalf.helpers.error_code.ErrorCode
        :param kwargs: The keyword-argument to format the ResponseError detail.
        :type kwargs: dict
        """
        if not isinstance(code, ErrorCode):
            self.internal_server_error()
            raise TypeError('Expected `code` to be of type gandalf.helpers.error_code.ErrorCode')
        error = ResponseErrors.response_for(code, **kwargs)
        self.logger.error(error)
        self.send_error(error['status'], data=error)

    def method_not_allowed_error(self, method):
        """
        Encapsulation method.
        Produce an error response when the required method is not allowed.
        """
        self.produce_error(ErrorCode.METHOD_NOT_ALLOWED, method=method)

    def internal_server_error(self):
        """
        Encapsulation method.
        Produce an error response when there is an internal server error.
        """
        self.produce_error(ErrorCode.INTERNAL_SERVER_ERROR, contact=self.contact)


def require_body(method):
    """
    Prepare POST, PUT and PATCH requests by checking a few parameters.
    Check the Content-Type header value which must be application/json*.
    Check that PUT and PATCH methods are not used on many-depth resource endpoints, see comment below.
    Check that the body exists.
    Decode the body from a JSON string to a Python dictionary.
    """
    def decorator(self, *args, **kwargs):
        if self.request.method not in ('POST', 'PUT', 'PATCH'):
            return

        content_type = self.request.headers.get('Content-Type', '')
        if not content_type.startswith(CONTENT_TYPE):
            return self.produce_error(ErrorCode.CONTENT_TYPE_HEADER_ERROR)

        # Check if a PUT or PATCH method is being applied to more than one-depth resources.
        # This is necessary since single-depth and many-depth resource endpoints share
        # the same Tornado handlers —see the example below— and if we want to be able to apply
        # PUT and PATCH methods to single-depth resources, there is no point in updating/replacing
        # a resource belonging to another resource —since we can already update/replace the resource
        # itself with its given ID.
        #
        # Example:
        # /gandalf/api/roles/{role_id} -> RoleHandler, we want to have PUT and PATCH methods here.
        # /gandalf/api/users/{user_id}/roles/{role_id} -> RoleHandler, we don't want PUT and PATCH methods here.
        if self.request.method in ('PUT', 'PATCH'):
            keys = list(self.path_kwargs.keys())
            if len(keys) > 1 and keys[0] in ('user_id', 'token_id', 'role_id') and keys[1] in ('role_id', 'permission_id'):
                return self.method_not_allowed_error(self.request.method)

        if not self.request.body:
            return self.produce_error(ErrorCode.MISSING_BODY)

        try:
            self.request.body = json.decode(self.request.body)
        except (TypeError, ValueError) as e:
            self.logger.error(e)
            self.internal_server_error()

        return method(self, *args, **kwargs)
    return decorator
