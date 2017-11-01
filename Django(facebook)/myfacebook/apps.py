from django.apps import AppConfig


class MyfacebookConfig(AppConfig):
    name = 'myfacebook'

    def ready(self):
        import myfacebook.signals
