from django.urls import path
from . import views

app_name = "rooms"

# <int:pk> 를 입력함으로서 url에 입력된 숫자를 pk로 인식해서 가져옴
# html에 넣을 argument는 <int:pk>의 pk가 넘어가는 것
urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]

