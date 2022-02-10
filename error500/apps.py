from django.apps import AppConfig


class Error500Config(AppConfig):
    name = 'error500'

    def ready(self):
        import error500.signals.got_request_exception  # noqa
