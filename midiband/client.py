# -*- coding: utf-8 -*-
import socket


class Client:
    config = {
        'server': None,
        'port': 65200,
        'name': None,
    }

    def __init__(self, server=None, port=65200):
        self.name = socket.gethostname()
