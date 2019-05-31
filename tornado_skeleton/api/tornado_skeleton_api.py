# coding: utf-8

import os

import tornado.web
from tornado import ioloop, log
from tradelab.config_object import ConfigObject
from tradelab.utils.decorators import retry_address_in_use

from tornado_skeleton.api.handlers import *


class URL(tuple):
    """
    Provide a tuple implementation to create Tornado handler signatures.
    """
    def __new__(cls, route, handler, initializers, **kwargs):
        """
        Create a new tuple of format (route, handler, initializers).
        The route is formatted with the given kwargs.

        :param route: A string representing the endpoint route,
                      accepting Python formatters.
        :type route: str
        :param handler: A handler class associated to the route,
                        it should be derivating from at least
                        tornado.web.RequestHandler and ideally
                        gandalf.api.handlers.BaseHandler.
        :type handler: tornado.web.RequestHandler
        :param initializers: Some initializers to pass to the handler
                             at initialization to use across all the
                             handler's methods.
        :type initializers: dict
        :param kwargs: Some keyword arguments to format the route.
        :type kwargs: dict
        """
        return tuple.__new__(cls, (route.format(**kwargs), handler, initializers))


class WebApplication(tornado.web.Application):
    """
    Gandalf Application overriding tornado.web.Application with Gandalf-related logic around handlers and initializers.
    """

    def __init__(self, initializers, session_factory, **kwargs):
        """
        Initialize the WebApplication object with handlers.
        The given initializers are bound to each handler.

        :param initializers: Some initializers to pass to the handler
                             at initialization to use across all the
                             handler's methods
        :type initializers: dict
        """
        base_url = initializers.get('base_url')

        handlers = [
            URL(r'{base_url}/?', MainHandler, initializers, base_url=base_url),
            URL(r'{base_url}/users/(?P<user_id>\d+)', UserHandler, initializers, base_url=base_url)
        ]

        super().__init__(handlers, session_factory=session_factory, **kwargs)


class TornadoSkeletonAPI(ConfigObject):
    """
    Entrypoint for the Gandalf API execution flow.
    This class inherits from tradelab.config_object.ConfigObject
    to support configuration management and manipulation.
    """

    def __init__(self, path=None, env=''):
        """
        Initialize the GandalfAPI object with a path and an environment for the configuration file.

        :param path: The path for the configuration file.
        :type path: str
        :param env: The environment of the API execution,
                    used to retrieve the correct configuration file.
        :type env: str
        """
        self.env = env
        filename = 'config/tornado_skeleton{}.yaml'.format(('.' + self.env) if self.env else '')
        if path:
            filename = os.path.join(path, filename)

        super().__init__(filename, raise_none=False)

        self.base_url = self.get('api:base_url')
        self.port = self.get('api:port')
        self.handlers_initializer = {
            'env': self.env,
            'contact': self.get('contact'),
            'base_url': self.get('api:base_url'),
            'api_version': self.get('api:version')
        }

    @retry_address_in_use(exception=OSError, count=10, delay=1, verbose=True)
    def start(self):
        """Start the API by loading the WebApplication object and creating an IO loop."""
        log.enable_pretty_logging()
        application = WebApplication(self.handlers_initializer, None, debug=self.get('debug'))
        application.listen(self.port)
        # _logger.info('Gandalf %sAPI running on port %s', self.env + ' ' if self.env else '', self.port)
        ioloop.IOLoop.current().start()
