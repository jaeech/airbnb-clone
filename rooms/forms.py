from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere", required=False)
    country = CountryField(default="KR").formfield(required=False)
    room_type = forms.ModelChoiceField(
        empty_label="Any Kind", queryset=models.RoomType.objects.all(), required=False
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = (
            "caption",
            "file",
        )

    # form 자체에는 room이 지정이 안되어있기 때문에
    # 실제로 저장이 이루어지기 전에, save method에 변형을 주어서
    # room을 지정해 준 후 저장!
    # views에서 보이는 room의 pk를 전달해주기 위해서 pk를 추가
    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        )

    # room을 저장하지 않고, views.py에 전달하기 위해서
    # 전달 후, room을 views.py 에서 저장 및 저장된 room으로 redirect
    # 가능하게 만들기 위해
    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room
