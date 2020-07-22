from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):
    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        # model 안에 있는 ForeignKey를 타고 들어가서
        # 그 안에 있는 model들을 가져올 수 있음
        # self.room.name
        return f"{self.review} - {self.room}"

    # Model에 직접 function을 만들어줘서 여러곳에서 사용가능하도록 만들 수 있음
    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6

        return round(avg, 2)

