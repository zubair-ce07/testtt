# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class TrainingAPIConfig(AppConfig):
    name = 'training_api'

    def ready(self):
        import training.signals