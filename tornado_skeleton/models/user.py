# coding: utf-8

import os
try:
    import ujson as json
except ImportError:
    import json


class User(object):
    def __init__(self):
        self.users = os.path.dirname(os.path.abspath(__file__)) + '/users.json'

    def get_users(self):
        with open(self.users) as f:
            return json.load(f)
