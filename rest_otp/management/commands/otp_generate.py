from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ...helpers import create_otp


class Command(BaseCommand):
    """
    Generate OTP secret for exiting users
    """

    def handle(self, *args, **options):

        for user in get_user_model().objects.all():
            create_otp(user, getattr(user, user.USERNAME_FIELD))
