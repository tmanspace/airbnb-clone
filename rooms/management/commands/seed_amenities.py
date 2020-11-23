from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):
    def handle(self, *args, **options):
        amenities = [
            "Air conditioning",
            "Breakfast",
            "Carbon monoxide alarm",
            "Crib",
            "Dryer",
            "Kitchen",
            "Shampoo",
            "Heating",
            "Washer",
            "Wifi",
            "Indoor fireplace",
            "Hangers",
            "Iron",
            "Hair dryer",
            "Dedicated workspace",
            "High chair",
            "Private bathroom",
            "Self check-in",
            "Smoke alarm",
            "TV",
        ]
        for a in amenities:
            Amenity.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Amenities created!"))
