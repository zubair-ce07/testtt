from django.apps import AppConfig


class TaskmanagerConfig(AppConfig):
    name = 'taskmanager'

    def ready(self):
        import taskmanager.signals