# command 만드는 방법
import random
from django.core.management.base import BaseCommand
from django_seed import Seed

# 중첩 List를 한번 벗겨주는 기능 flatten
from django.contrib.admin.utils import flatten
from rooms import models as room_models
from users import models as user_models
from lists import models as list_models


class Command(BaseCommand):

    help = "This command seeds many lists"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many lists do you want to create",
        )

    def handle(self, *args, **options):
        # argument의 number를 받아옴
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        # 전체 room 내역을 전부다 하고 하면 [숫자:숫자] 하면 됨
        all_rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List,
            number,
            # host랑 room_type을 설정해줘야해서 랜덤으로 불러옴
            # faker의 기능을 사용함
            {"user": lambda x: random.choice(all_users),},
        )
        created_lists = seeder.execute()
        pk_of_created_lists = flatten(created_lists.values())

        for pk in pk_of_created_lists:
            list_name = list_models.List.objects.get(pk=pk)
            to_add = all_rooms[random.randint(0, 5) : random.randint(6, 35)]
            list_name.rooms.add(*to_add)

            # 요렇게 해도 되고 seed_rooms에서 했던 것 처럼
            # for r in all_rooms:
            #     random_number = random.randint(0, 60)
            #     if random_number % 7 == 1:
            #         list_name.rooms.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} reviews created"))
