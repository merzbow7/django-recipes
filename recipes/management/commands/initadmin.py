import environ
from django.contrib.auth.models import User
from django.core.management import BaseCommand

env = environ.Env()


class Command(BaseCommand):
    help = 'Init superuser'

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = env.get_value("ADMIN_USERNAME")
            password = env.get_value("ADMIN_PASSWORD")
            admin = User.objects.create_superuser(
                username=username,
                email="email@example.com",
                password=password,
                is_staff=True,
                is_active=True,
                is_superuser=True
            )
            admin.save()
