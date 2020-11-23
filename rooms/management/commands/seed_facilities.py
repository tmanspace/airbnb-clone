from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    def handle(self, *args, **options):
        facilities = [
            "Gym",
            "Parking",
            "Elevator",
            "Paid parking off premises",
            "Paid parking on premises",
            "Private entrance",
            "Parking",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS("Facilities created!"))
