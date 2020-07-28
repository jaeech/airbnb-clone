from django.views.generic import ListView
from . import models


class HomeView(ListView):
    """ HomeView Definition"""

    model = models.Room
    paginate_by = 10
    parginate_orphans = 5
    ordering = "created"
    # page를 위한 키워드도 지정 가능
    # 아니면 자동으로 됨
    # page_kwarg = "anykeyword"

