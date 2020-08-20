from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms


class HomeView(ListView):
    """ HomeView Definition"""

    model = models.Room
    paginate_by = 12
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

                paginator = Paginator(qs, 12, orphans=4)

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

                paginator = Paginator(qs, 12, orphans=4)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()
            return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
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

    def get_object(self, queryset=None):
        # 지금 있는 페이지의 Room을 확인 후
        # Room 주인이랑 접속해있는 User랑 비교 후
        # 본인 소유가 아니면 HTTP404 Error Raise
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        # 지금 있는 페이지의 Room을 확인 후
        # Room 주인이랑 접속해있는 User랑 비교 후
        # 본인 소유가 아니면 HTTP404 Error Raise
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


# login 했을때만 적용되는거
@login_required
# request에 추가로 받아올 내역들 room_pk photo_pk가 있으니까
def delete_photo(request, room_pk, photo_pk):
    # 현재 로그인되어있는 user 확인
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        # 로그인 되어있는 user랑 room 주인과 비교
        if room.host.pk != user.pk:
            messages.error(request, "No permission to delete taht photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo deleted")
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))
    return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    fields = ("caption",)
    pk_url_kwarg = "photo_pk"
    success_message = "Photo updated"

    # 성공한 후, URL redirct를 위해서,
    # room_pk 를 넣어주기 위해서는 method를 사용해야함
    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})

    def get_object(self, queryset=None):
        # 지금 있는 페이지의 Room을 확인 후
        # Room 주인이랑 접속해있는 User랑 비교 후
        # 본인 소유가 아니면 HTTP404 Error Raise
        photo = super().get_object(queryset=queryset)
        if photo.room.host.pk != self.request.user.pk:
            raise Http404()
        return photo


class AddPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, FormView):

    model = models.Photo
    template_name = "rooms/photo_create.html"
    fields = ("caption", "file")
    form_class = forms.CreatePhotoForm

    # from.py에 pk를 전달해주기 위해서
    # form valid를 불러 온후, pk를 전달
    # form_valid는 항상 HTTP response를 필요로 함
    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))

