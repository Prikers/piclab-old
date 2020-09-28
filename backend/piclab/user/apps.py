from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'piclab.user'

    def ready(self):
        import piclab.user.signals
