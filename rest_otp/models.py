from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .app_settings import QR_VERSION, QR_BOX_SIZE, QR_BORDER

import pyotp
import qrcode

import base64
from io import BytesIO


class Otp(models.Model):
    """
    OTP model
    Store secret of every generated otp
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='otp',
        on_delete=models.CASCADE
    )
    secret = models.CharField(_('secret'), max_length=50)
    name = models.CharField(
        _('account name'),
        max_length=50,
        help_text=_('Account Name for Provisioning URI, '
                    'to be used when need URI for QR code.')
    )
    issuer_name = models.CharField(
        _('issuer name'),
        max_length=50,
        help_text=_('Issuer Name for Provisioning URI.')
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = _('otp')

    def __str__(self):
        return self.secret

    def get_otp_code(self) -> str:
        """
        Get current otp code
        """
        return pyotp.TOTP(self.secret).now()

    def get_otp_uri(self) -> str:
        """
        Get otp uri
        """
        return pyotp.totp.TOTP(self.secret).provisioning_uri(
            self.name, issuer_name=self.issuer_name
        )

    def get_qr_code(self):
        """
        Get QR code from otp uri
        """
        qr = qrcode.QRCode(
            version=QR_VERSION,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=QR_BOX_SIZE,
            border=QR_BORDER
        )
        qr.add_data(self.get_otp_uri())
        qr.make(fit=True)
        img = qr.make_image()

        output = BytesIO()
        img.save(output)
        qr_data = output.getvalue()
        output.close()

        return base64.b64encode(qr_data).decode('ascii')


class RecoveryCode(models.Model):
    """
    Recovery codes for 2FA
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='recovery_codes',
        on_delete=models.CASCADE
    )
    code = models.CharField(_('code'), max_length=12, unique=True)
    is_enable = models.BooleanField(_('enable'), default=True)

    class Meta:
        verbose_name = _('recovery code')
        verbose_name_plural = _('recovery codes')

    def __str__(self):
        return self.code
