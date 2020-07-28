from math import ceil
from django.shortcuts import render
from . import models


def all_rooms(request):
    # page key가 없을 경우에 page=1 을 자동적용
    page = request.GET.get("page", 1)
    # page 자체를 숫자로 적용시켜주고
    # page의 value가 지정 되어 있지 않을 경우에 page=1로 자동 지정
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size

    # html파일 지정 및 context를 통해 html에 변수 전달
    all_rooms = models.Room.objects.all()[offset:limit]

    page_count = ceil(models.Room.objects.count() / page_size)

    # 변수 생성 후, {dict 형식으로 변수 전달}
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )
