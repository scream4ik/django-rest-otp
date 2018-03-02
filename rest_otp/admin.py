from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Otp, RecoveryCode


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('user', 'secret', 'otp_code')

    def otp_code(self, obj):
        return obj.get_otp_code()

    otp_code.short_description = _('otp code')


@admin.register(RecoveryCode)
class RecoveryCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'is_enable')
    list_filter = ('is_enable',)
