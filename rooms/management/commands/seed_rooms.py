import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms you want to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        # all()은 좋은 방법은 아님. 여기서는 초기 50개 정도니까 all을 사용.
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        print(room_types, all_users)
        seeder.add_entity(
            room_models.Room,
            number, {
                'name': lambda x: seeder.faker.address(),
                'host': lambda x: random.choice(all_users),
                'room_type': lambda x: random.choice(room_types),
                'price': lambda x: random.randint(1, 300),
                'guests': lambda x: random.randint(1, 20),
                'beds': lambda x: random.randint(1, 5),
                'bedrooms': lambda x: random.randint(1, 5),
                'baths': lambda x: random.randint(1, 5),
            },
        )
        created_photos = seeder.execute()
        # seeder.execute()로 반환되는 값은 2차원 배열이므로 1차원 리스트로 바꿔준다.
        # 예를 들면 [[13, 14, 15]] 이런식으로 출력되는 pk값을 [13, 14, 15] 이렇게 바꿔줌.
        created_clean = flatten(list(created_photos.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                print(f"사진 {i-2}개 만드는 중")
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                print(f"매직넘버 = {magic_number}")
                if magic_number % 2 == 0:
                    # many to many field에서 뭔가를 추가하는 방법
                    room.amenities.add(a)

            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in house_rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
