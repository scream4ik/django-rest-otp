from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .helpers import create_otp, create_recovery


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
        for i in range(16):
            create_recovery(instance)
