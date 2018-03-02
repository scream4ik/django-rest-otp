from django.apps import AppConfig


class RestOtpConfig(AppConfig):
    name = 'rest_otp'

    def ready(self):
        import rest_otp.signals  # noqa
