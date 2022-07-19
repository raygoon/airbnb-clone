import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models

SEED_NAME = "reservations"


class Command(BaseCommand):

    help = "This command creates {SEED_NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many {SEED_NAME}?"
        )

    def handle(self, *args, **options):

        def reservation_date():
            in_date = datetime.now() + timedelta(days=random.randint(-10, 5))
            global out_date
            out_date = in_date + timedelta(days=random.randint(0, 25))
            print(f"시작일은{in_date} 종료일은{out_date}")
            return [in_date, out_date]

        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(
                    ["pending", "confirmed", "canceled"]
                    ),
                "check_in": lambda x: reservation_date()[0],
                "check_out": lambda x: out_date,
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms)
            },
        )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {SEED_NAME} created!"))
