import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command adds rooms how much you wish"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many rooms to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "city": lambda x: seeder.faker.city(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(50, 200),
                "beds": lambda x: random.randint(1, 5),
                "guests": lambda x: random.randint(1, 6),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} rooms were created!"))
