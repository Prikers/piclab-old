from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'piclab.api'

    def ready(self):
        import piclab.api.signals
