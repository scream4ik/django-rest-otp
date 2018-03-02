from django.conf import settings

from .utils import import_callable
from .serializers import JWTSerializer


ISSUER_NAME = getattr(settings, 'REST_OTP_ISSUER_NAME', 'Secure App')
REDIS_URL = getattr(settings, 'REST_OTP_REDIS_URL', 'redis://localhost:6379/0')
JWT_SERIALIZER = import_callable(
    getattr(settings, 'REST_OTP_JWT_SERIALIZER', JWTSerializer)
)
