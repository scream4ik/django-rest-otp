from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from .models import Otp, RecoveryCode
from .app_settings import ISSUER_NAME, REDIS_URL, ALLOWED_CHARS

import pyotp
from redis_collections import Dict
from redis import StrictRedis
from redis.client import Redis


def get_redis_connection() -> Redis:
    """
    Return a Redis client object configured from the given URL
    """
    return StrictRedis.from_url(REDIS_URL)


def get_2fa_otp_dict() -> Dict:
    """
    Function return dict from redis with otp data
    """
    return Dict(key='2fa_otp', redis=get_redis_connection())


def get_2fa_recovery_code_dict() -> Dict:
    """
    Function return dict from redis with recovery code data
    """
    return Dict(key='2fa_recovery_code', redis=get_redis_connection())


def create_otp(user: get_user_model(), name: str) -> Otp:
    """
    Function create OTP secret
    """
    return Otp.objects.create(
        user=user,
        secret=pyotp.random_base32(),
        name=name,
        issuer_name=ISSUER_NAME
    )


def create_recovery(user: get_user_model()) -> RecoveryCode:
    """
    Function create recovery code
    """
    return RecoveryCode.objects.create(
        user=user, code=get_random_string(allowed_chars=ALLOWED_CHARS)
    )


def tmp_user_id(user_id: int) -> dict:
    """
    Function generate temp user id and save to redis.
    It's need for associate OTP form with user
    """
    otp_user_id = get_random_string()
    recovery_user_id = get_random_string()

    data = get_2fa_otp_dict()
    data[otp_user_id] = user_id
    data = get_2fa_recovery_code_dict()
    data[recovery_user_id] = user_id

    return {'otp': otp_user_id, 'recovery': recovery_user_id}


def jwt_encode(user):
    try:
        from rest_framework_jwt.settings import api_settings
    except ImportError:
        raise ImportError("djangorestframework_jwt needs to be installed")

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)
