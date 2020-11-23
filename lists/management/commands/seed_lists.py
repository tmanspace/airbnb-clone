import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists.models import List
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command adds lists how much you wish"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many lists to create?"
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
        created_lists = seeder.execute()
        created_clean = flatten(list(created_lists.values()))
        for pk in created_clean:
            list_ = List.objects.get(pk=pk)
            to_add = rooms_all[random.randint(0, 5) : random.randint(6, 20)]
            list_.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} lists were created!"))
