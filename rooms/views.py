from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms


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


class SearchView(View):
    """ Search Rooms """

    def get(self, request):

        # rooms/search url로 직접 갈 경우를 위해
        # 임시방편으로 unbounded form으로 돌려줌
        # 그 경우에는 GET을 줄 수 없기 때문에
        # country가 필수인 관계로
        # country가 있으면과 없으면으로 분리
        country = request.GET.get("country")
        city = request.GET.get("city")
        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                # filtering을 위한 argument를 모으는 것
                # argument의 앞에 이름은 model의 이름을 따라야 함
                # model 항목 내에 들어가고 싶으면 __ 를 붙여줘야함
                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                # filter를 위한 QuerySet/argutments
                # Paginator를 사용하려면 order가 있는 QuerySet이여야 함
                qs = models.Room.objects.filter(**filter_args).order_by("created")

                paginator = Paginator(qs, 3, orphans=1)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)
                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        elif city:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                # filtering을 위한 argument를 모으는 것
                # argument의 앞에 이름은 model의 이름을 따라야 함
                # model 항목 내에 들어가고 싶으면 __ 를 붙여줘야함
                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                qs = models.Room.objects.filter(**filter_args).order_by("created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()
            return render(request, "rooms/search.html", {"form": form})

