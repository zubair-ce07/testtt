from __future__ import absolute_import
from django.apps import AppConfig


class TaskManagerConfig(AppConfig):
    name = 'taskmanager'

    def ready(self):
        import taskmanager.signals
        import taskmanager.tasks
