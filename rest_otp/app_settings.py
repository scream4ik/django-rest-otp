from django.conf import settings


ISSUER_NAME = getattr(settings, 'REST_OTP_ISSUER_NAME', 'Secure App')
REDIS_URL = getattr(settings, 'REST_OTP_REDIS_URL', 'redis://localhost:6379/0')
RECOVERY_CODES_RANGE = getattr(settings, 'REST_OTP_RECOVERY_CODES_RANGE', 16)
QR_VERSION = getattr(settings, 'REST_OTP_QR_VERSION', 1)
QR_BOX_SIZE = getattr(settings, 'REST_OTP_QR_BOX_SIZE', 10)
QR_BORDER = getattr(settings, 'REST_OTP_QR_BORDER', 4)
