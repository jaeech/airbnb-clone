# command 만드는 방법
import random
from django.core.management.base import BaseCommand

# 중첩 List를 한번 벗겨주는 기능 flatten
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command seeds many rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many rooms do you want to create"
        )

    def handle(self, *args, **options):
        # argument의 number를 받아옴
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            # host랑 room_type을 설정해줘야해서 랜덤으로 불러옴
            # faker의 기능을 사용함
            {
                "name": lambda x: seeder.faker.city(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(50, 300),
                "beds": lambda x: random.randint(1, 3),
                "bedrooms": lambda x: random.randint(1, 3),
                "baths": lambda x: random.randint(1, 2),
                "guests": lambda x: random.randint(1, 6),
            },
        )
        # seeder를 실행하면서, 이를 created_rooms 변수에 저장
        created_rooms = seeder.execute()
        # 생성된 room의 각 pk(id)를 가져오기 (List 형태로)
        # flatten은 중첩된 리스트를 한단계 풀기 위해 적용
        ids_from_created_rooms = flatten(created_rooms.values())

        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        # 생성된 각 Room에 대해 포토를 저장하기
        for pk in ids_from_created_rooms:
            # pk(id) 번호에 대한 이름을 추출하기
            room_name = room_models.Room.objects.get(pk=pk)

            # room 에 대한 photo를 random한 숫자만큼 만들기
            for i in range(2, random.randint(3, 20)):
                # photo 생성은 seeder랑 다른 형태로 생성되어야 함
                # objects.create() 형식으로
                # ForeignKey을 가지는 object에 대한 생성방식
                room_models.Photo.objects.create(
                    caption=seeder.faker.city(),
                    file=f"/room_photos/{random.randint(1,30)}.webp",
                    room=room_name,
                )

            # many to many relation의 경우, 하기와 같이 랜덤 선택 가능
            for a in amenities:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    room_name.amenities.add(a)

            for f in facilities:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    room_name.facilities.add(f)

            for h in rules:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    room_name.house_rules.add(h)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created"))
