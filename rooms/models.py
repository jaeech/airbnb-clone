from django.db import models

# url의 이름을 받아서 해당 이름에 맞느 url을 불러오는 기능
from django.urls import reverse

# django_countries 라이브러리를 다운받아서 사용
from django_countries.fields import CountryField

# users.models 에서 User 이름을 가져옴
# (하지만 연결을 string 형태로 지정하면, 하기 import 필요없음)
# from users import models as user_models


# 생성한 core app 에서 models를 가져와서 core_modles로 명명하여 사용
from core import models as core_models

# 이름을 저장해놓기 위해 만들어놓은 class
class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 위에 만들어놓은  AcstractItem class 를 사용하여 RoomType을 생성함
class RoomType(AbstractItem):
    """ RoomTpe Model Definition"""

    class Meta:
        # 보여지는 이름을 바꿈
        verbose_name = "Room Type"


class Amenity(AbstractItem):
    """ Amenity Model Definition"""

    class Meta:
        # 자동으로 변경되는 복수형을 바꿔줌
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """ HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    # 어느폴더에 저장할 것인지 지정
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    # Admin에 보여지는 명칭을 지정해주기 위해
    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # users.models 에서 User 이름을 가져옴
    # models.CASCADE 는, user가 지워지면 room도 지워지는 폭포수형태로 연결
    # Key를 불러오는 값은 String 형태로도 가능
    # String 형태로 가져오면, module을 import 할 필요도 없음
    host = models.ForeignKey(
        # related_name을 입력해줌으로서, Qeuryset에서 _set 형태가 아닌
        # 설정한 이름으로 찾기 쉽게 만들기
        "users.User",
        related_name="rooms",
        on_delete=models.CASCADE,
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    # Admin에 보여지는 명칭을 지정해주기 위해
    def __str__(self):
        return self.name

    # 저장 시, 내용을 변경해서 저장하고 싶을 경우에
    # super()를 이용해 변경하는것
    # save()는 django의 save method를 가져와서 변경하는 것
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # Call the real save() method  #

    # admin 페이지에서 ROOM의 실제 페이지에 접속 가능하게 만드는
    # View on Site 기능을 만듦
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        # Room.objects를 하기와 같이 그냥 self로 표현가능
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def first_photo(self):
        photo = self.photos.all()[0]
        return photo.file.url

    def get_next_four_photos(self):
        photo = self.photos.all()[1:5]
        return photo
