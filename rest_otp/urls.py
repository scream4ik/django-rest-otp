from django.urls import path

from .views import (
    OtpUserView, RecoveryCodeListView, LoginOtpView, LoginRecoveryCodeView
)


urlpatterns = [
    path('totp/', OtpUserView.as_view(), name='user_totp'),
    path(
        'recovery-codes/',
        RecoveryCodeListView.as_view(),
        name='recovery_codes'
    ),
    path('login/otp/', LoginOtpView.as_view(), name='login_otp'),
    path(
        'login/recovery-code/',
        LoginRecoveryCodeView.as_view(),
        name='login_recovery_code'
    ),
]
