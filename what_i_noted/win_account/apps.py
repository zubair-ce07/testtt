from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'win_account'

    def ready(self):
        import win_account.signals
