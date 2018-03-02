from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ...helpers import create_recovery


class Command(BaseCommand):
    """
    Generate recovery codes for exiting users
    """

    def handle(self, *args, **options):

        for user in get_user_model().objects.all():
            create_recovery(user)
