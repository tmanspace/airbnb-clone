import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists.models import List
from users import models as user_models
from rooms import models as room_models

TEXT = "lists"


class Command(BaseCommand):

    help = f"This command adds {TEXT} how much you wish"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many {TEXT}  to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users_all = user_models.User.objects.all()
        rooms_all = room_models.Room.objects.all()
        seeder.add_entity(
            List,
            number,
            {
                "name": lambda x: seeder.faker.word(),
                "user": lambda x: random.choice(users_all),
            },
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_ = List.objects.get(pk=pk)
            to_add = rooms_all[1 : random.randint(6, 20)]
            list_.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} {TEXT} were created!"))
