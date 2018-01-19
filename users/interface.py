# -*- coding: utf-8 -*-

import json
from django.db import models

class Status:
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon

    def deserved_status(self):
        pass