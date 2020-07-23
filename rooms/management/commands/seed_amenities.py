## command 만드는 방법
from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):

    help = "This command seeds the amenities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times", help="How many times do you want me to repeat"
    #     )

    def handle(self, *args, **options):
        amenities = [
            "Kitchen",
            "Shampoo",
            "Heating",
            "Washer",
            "WiFi",
            "Indoor fireplace",
            "Iron",
            "Laptop friendly workplace",
            "Crib",
            "Self check-in",
            "Carbon monoxide detector",
            "Air conditioning",
            "Dryer",
            "Breakfast",
            "Hangers",
            "Hair Dryer",
            "TV",
            "High chair",
            "Smoke detector",
            "Private bathroom",
        ]

        for a in amenities:
            Amenity.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS("Amenities created"))
