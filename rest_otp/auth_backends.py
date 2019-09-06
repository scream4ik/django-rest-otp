from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from .models import RecoveryCode
from .helpers import get_2fa_otp_dict, get_2fa_recovery_code_dict


class OtpAuthenticationBackend(ModelBackend):
    """
    Auth backend for identify user by OTP code
    """
    def authenticate(self, request, **credentials):
        user = None
        tmp_user_id = credentials.get('tmp_user_id')
        otp_code = credentials.get('otp_code')

        data = get_2fa_otp_dict()

        if tmp_user_id in data:
            user = get_user_model().objects.get(pk=data.get(tmp_user_id))

            if user.otp.get_otp_code() != otp_code:
                return None

        try:
            del data[tmp_user_id]
        except KeyError:
            pass
        return user


class RecoveryCodeAuthenticationBackend(ModelBackend):
    """
    Auth backend for identify user by recovery code
    """
    def authenticate(self, request, **credentials):
        user = None
        tmp_user_id = credentials.get('tmp_user_id')
        recovery_code = credentials.get('recovery_code')

        data = get_2fa_recovery_code_dict()

        if tmp_user_id in data:
            try:
                user = get_user_model().objects.get(pk=data.get(tmp_user_id))

                code = RecoveryCode.objects.get(
                    user=user, code=recovery_code, is_enable=True
                )
                code.is_enable = False
                code.save(update_fields=['is_enable'])

            except RecoveryCode.DoesNotExist:
                pass

        try:
            del data[tmp_user_id]
        except KeyError:
            pass
        return user
