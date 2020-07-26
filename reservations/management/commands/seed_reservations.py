# command 만드는 방법
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
from reservations import models as reservations_models


NAME = "reservations"


class Command(BaseCommand):

    help = f"This command seeds many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"How many {NAME} do you want to create",
        )

    def handle(self, *args, **options):
        # argument의 number를 받아옴
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        # 전체 room 내역을 전부다 하고 하면 [숫자:숫자] 하면 됨
        all_rooms = room_models.Room.objects.all()
        seeder.add_entity(
            reservations_models.Reservation,
            number,
            # host랑 room_type을 설정해줘야해서 랜덤으로 불러옴
            # faker의 기능을 사용함
            {
                "status": lambda x: random.choice(
                    ["pending", "confirmed", "cancelled"]
                ),
                "guest": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
                "check_in": datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(2, 5)),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
