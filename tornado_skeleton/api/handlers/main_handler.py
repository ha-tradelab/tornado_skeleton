# coding: utf-8

from tornado_skeleton.api.handlers.base_handler import BaseHandler


class MainHandler(BaseHandler):
    def get(self):
        self.send_response({'status': 'Alive'})
