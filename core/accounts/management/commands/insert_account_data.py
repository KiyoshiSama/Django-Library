from faker import Faker
from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "creating fake accounts..."

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        User.objects.create_user(
            email=self.fake.email(),
            password=self.fake.password(
                length=10,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ),
        )
