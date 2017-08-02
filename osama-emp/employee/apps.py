from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    name = 'employee'

    def ready(self):
        from . import signals
