from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="csu@mail.ru",
            first_name="dred",
            last_name="Home",
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )

        user.set_password("12qwe34")
        user.save()
