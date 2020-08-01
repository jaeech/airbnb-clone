from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):
    """ HomeView Definition"""

    model = models.Room
    paginate_by = 10
    parginate_orphans = 5
    ordering = "created"
    # object_list의 명칭을 직정해줄 수 있음
    context_object_name = "rooms"
    # page를 위한 키워드도 지정 가능
    # 아니면 자동으로 됨
    # page_kwarg = "anykeyword"


class RoomDetail(DetailView):
    """ RoomDetail Definition"""

    model = models.Room
    # pk를 바꿀 수도 있음
    # pk_url_kwarg = "potato"


def search(request):
    # city=입력이 없을 경우 Anywhere로 셋팅되게
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    # pk는 int임으로 변경 필요
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    room_type = int(request.GET.get("room_type", 0))
    # 여러개의 내역을 받아야하는데 리스트로 받아야해서
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "super_host": super_host,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }
    # **로 dict 안에 있는 내용을 unpack 해줌
    return render(request, "rooms/search.html", {**form, **choices})

