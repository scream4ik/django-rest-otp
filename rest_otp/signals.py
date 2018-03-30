from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .helpers import create_otp, create_recovery
from .app_settings import RECOVERY_CODES_RANGE, CREATE_RECOVERY_CODE_FUNCTION


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_otp_handler(sender, instance=None, created=False, **kwargs):
    """
    Signal create OTP secret for new user
    """
    if created:
        create_otp(instance, getattr(instance, instance.USERNAME_FIELD))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_recovery_handler(sender, instance=None, created=False, **kwargs):
    """
    Signal create recovery codes for new user
    """
    if created:
        for i in range(RECOVERY_CODES_RANGE):
            if CREATE_RECOVERY_CODE_FUNCTION is not None:
                CREATE_RECOVERY_CODE_FUNCTION(instance)
            else:
                create_recovery(instance)
