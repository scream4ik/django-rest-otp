from rest_framework import generics, permissions, status
from rest_framework.response import Response

from django.contrib.auth import login as django_login
from django.conf import settings

from .serializers import (
    OtpSerializer,
    RecoveryCodeSerializer,
    LoginOtpSerializer,
    LoginRecoveryCodeSerializer
)
from .models import Otp, RecoveryCode
from .helpers import jwt_encode
from .utils import import_callable
from .serializers import JWTSerializer

try:
    from drf_yasg.utils import swagger_auto_schema
except ImportError:
    from .decorators import dummy_auto_schema as swagger_auto_schema

JWT_SERIALIZER = import_callable(
    getattr(settings, 'REST_OTP_JWT_SERIALIZER', JWTSerializer)
)


class OtpUserView(generics.RetrieveAPIView):
    """
    Endpoint for current user otp data
    """
    serializer_class = OtpSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return Otp.objects.get(user=self.request.user)


class RecoveryCodeListView(generics.ListAPIView):
    """
    Endpoint for current user recovery codes list
    """
    serializer_class = RecoveryCodeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return RecoveryCode.objects.filter(user=self.request.user)


class LoginView(generics.GenericAPIView):
    """
    Base view for login view
    """
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses={200: JWT_SERIALIZER})
    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(
            data=request.data, context={'request': request}
        )
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token = jwt_encode(self.user)
        django_login(self.request, self.user)

    def get_response(self):
        data = {
            'user': self.user,
            'token': self.token
        }
        serializer = JWT_SERIALIZER(
            instance=data, context={'request': self.request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginOtpView(LoginView):
    """
    Endpoint for login user by OTP code

    If user enable 2FA when he send login and password, backend return tmp code

    And then you need send tmp code from login endpoint and OTP code from
    mobile app
    """
    serializer_class = LoginOtpSerializer


class LoginRecoveryCodeView(LoginView):
    """
    Endpoint for login user by recovery code

    If user enable 2FA when he send login and password, backend return tmp code

    And then you need send tmp code from login endpoint with recovery code
    """
    serializer_class = LoginRecoveryCodeSerializer
