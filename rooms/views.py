from django.views.generic import ListView
from django.http import Http404

# from django.urls import reverse
# redirect 추가하여 사용도 가능
from django.shortcuts import render
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


# pk의 경우, urls.py에 입력해놓은 path("<int:pk>" 의 명칭과 동일하게 가야함
# pk는 URL에 입력된 rooms 뒤에 입력된 url 내 숫자를 받아오게 됨
def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404()
        # Error 발생 시 home으로 redirect도 가능
        # return redirect(reverse("core:home"))
