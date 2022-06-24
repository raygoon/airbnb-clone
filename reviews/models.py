from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """Reviews Model Definition"""

    review = models.TextField()
    Accuracy = models.IntegerField()
    Communication = models.IntegerField()
    Cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.review}-{self.room}"