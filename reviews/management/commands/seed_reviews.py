import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command adds reviews how much you wish"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many reviews to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users_all = user_models.User.objects.all()
        rooms_all = room_models.Room.objects.all()
        seeder.add_entity(
            Review,
            number,
            {
                "review": lambda x: seeder.faker.sentence(),
                "accuracy": lambda x: random.randint(1, 5),
                "communication": lambda x: random.randint(1, 5),
                "cleanliness": lambda x: random.randint(1, 5),
                "location": lambda x: random.randint(1, 5),
                "check_in": lambda x: random.randint(1, 5),
                "value": lambda x: random.randint(1, 5),
                "room": lambda x: random.choice(rooms_all),
                "user": lambda x: random.choice(users_all),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews were created!"))
