import random
from datetime import datetime, timedelta


def check_date(first, second):
    mydate = datetime.now() + timedelta(days=random.randint(first, second))
    return mydate


datas = {
    "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
    "check_in": lambda x: check_date(0, 7),
    "check_out": lambda x: check_date(x + 3, x + 20),
    "guest": lambda x: random.choice(users),
    "room": lambda x: random.choice(rooms),
}

print(ord(datas['check_out']))
