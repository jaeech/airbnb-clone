from django.shortcuts import render
from . import models


def all_rooms(request):
    # html파일 지정 및 context를 통해 html에 변수 전달
    all_rooms = models.Room.objects.all()

    # 변수 생성 후, {dict 형식으로 변수 전달}
    return render(request, "rooms/home.html", context={"rooms": all_rooms,})
