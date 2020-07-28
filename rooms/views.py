from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from . import models


def all_rooms(request):
    # page key가 없을 경우에 page=1 을 자동적용
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        # page는 get_page와 다르게 Error Handling이 수동으로 이루어져야 함
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": rooms})

    except Exception:
        # 기본페이지로 이동
        return redirect("/")
