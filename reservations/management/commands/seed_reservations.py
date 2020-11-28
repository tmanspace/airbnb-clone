import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations.models import Reservation
from users import models as user_models
from rooms import models as room_models

TEXT = "reservations"


class Command(BaseCommand):

    help = f"This command adds {TEXT} how much you wish"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help=f"How many {TEXT} to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users_all = user_models.User.objects.all()
        rooms_all = room_models.Room.objects.all()
        seeder.add_entity(
            Reservation,
            number,
            {
                "guest": lambda x: random.choice(users_all),
                "room": lambda x: random.choice(rooms_all),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
                "status": lambda x: random.choice(
                    [
                        "pending",
                        "confirmed",
                        "canceled",
                    ]
                ),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {TEXT} were created!"))
