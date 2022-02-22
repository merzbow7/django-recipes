import environ
from django.contrib.auth.models import User
from django.core.management import BaseCommand

env = environ.Env()


class Command(BaseCommand):
    """Create initadmin for manage.py."""

    help = 'Init superuser'

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = env.get_value('ADMIN_USERNAME')
            password = env.get_value('ADMIN_PASSWORD')
            email = env.get_value('ADMIN_EMAIL')
            admin = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_active=True,
                is_superuser=True,
            )
            admin.save()
