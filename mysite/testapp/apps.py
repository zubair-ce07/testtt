# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class TestappConfig(AppConfig):
    name = 'testapp'

    def ready(self):
    	import testapp.signals
