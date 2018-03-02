from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

from .models import Otp, RecoveryCode
from .utils import import_callable


class OtpSerializer(serializers.ModelSerializer):
    """
    Serializer for user otp
    """
    otp_uri = serializers.CharField(source='get_otp_uri')
    qr_code = serializers.CharField(source='get_qr_code')

    class Meta:
        model = Otp
        fields = '__all__'


class RecoveryCodeSerializer(serializers.ModelSerializer):
    """
    Serializer for user recovery codes list
    """
    class Meta:
        model = RecoveryCode
        fields = ('code', 'is_enable')


class LoginOtpSerializer(serializers.Serializer):
    """
    Serializer for auth user by OTP
    """
    tmp_user_id = serializers.CharField()
    otp_code = serializers.CharField()

    def validate(self, attrs):
        tmp_user_id = attrs.get('tmp_user_id')
        otp_code = attrs.get('otp_code')

        user = authenticate(
            request=self.context['request'],
            tmp_user_id=tmp_user_id,
            otp_code=otp_code
        )

        if user is None:
            raise serializers.ValidationError(
                _('Unable to log in with provided credentials.')
            )

        if not user.is_active:
            raise serializers.ValidationError(_('User account is disabled.'))

        attrs['user'] = user
        return attrs


class LoginRecoveryCodeSerializer(serializers.Serializer):
    """
    Serializer for auth user by recovery code
    """
    tmp_user_id = serializers.CharField()
    recovery_code = serializers.CharField()

    def validate_recovery_code(self, value):
        try:
            # more effective check in auth backend
            RecoveryCode.objects.get(code=value, is_enable=True)
        except RecoveryCode.DoesNotExist:
            raise serializers.ValidationError(_('Wrong recovery code'))
        return value

    def validate(self, attrs):
        tmp_user_id = attrs.get('tmp_user_id')
        recovery_code = attrs.get('recovery_code')

        user = authenticate(
            request=self.context['request'],
            tmp_user_id=tmp_user_id,
            recovery_code=recovery_code
        )

        if user is None:
            raise serializers.ValidationError(
                _('Unable to log in with provided credentials.')
            )

        if not user.is_active:
            raise serializers.ValidationError(_('User account is disabled.'))

        attrs['user'] = user
        return attrs


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email',)


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """
        Required to allow using custom REST_OTP_USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        JWTUserDetailsSerializer = import_callable(
            getattr(
                settings,
                'REST_OTP_USER_DETAILS_SERIALIZER',
                UserDetailsSerializer
            )
        )
        user_data = JWTUserDetailsSerializer(
            obj['user'], context=self.context
        ).data
        return user_data
