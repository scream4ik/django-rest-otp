from django.conf import settings


ISSUER_NAME = getattr(settings, 'REST_OTP_ISSUER_NAME', 'Secure App')
REDIS_URL = getattr(settings, 'REST_OTP_REDIS_URL', 'redis://localhost:6379/0')
