from django.views.generic import ListView, DetailView
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

