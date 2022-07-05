from django.db import models
from django_countries.fields import CountryField
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "RoomType"
        ordering = ["name"]


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"

    pass


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "HouseRule"


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField()

    # 파이썬 코드는 수직해석이라서 Room 클래스의 뒤쪽에 있어야 하지만,
    # 클래스 코드의 위치를 변경하지 않고 아래처럼 클래스네임을 string으로 처리하는 방법을 사용할 수 있다. ("Room")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    # 호스트는 유저이기도 하다 이처럼 특정데이터베이스와 다른 데이터베이스를 연결하려 할때는
    # Foreignkey 를 사용해서 연결해준다.
    # on_delete=models.CASCADE 는 User에 종속된 모든 데이터베이스 필드의 정보들은 User 가 삭제되면 같이 삭제된다는 뜻이다.
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )

    # Foreinkey 는 Field가 1대다 의 관계일때 ManyToManyField 는 다대다의 관계일때 사용한다.
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    # Rooms model row 위쪽에 나오는 Rooms Object ID 대신 user 이름이 나오도록 __str__을 사용해서 아래와 같이 세팅해 줄수 있다.
    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
        return all_ratings / len(all_reviews)
