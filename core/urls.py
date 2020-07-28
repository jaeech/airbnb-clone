from django.urls import path
from rooms import views as room_views

# app_name은  config.urls.py 내에 있는 namespace 명칭과 동일해야함
app_name = "core"

urlpatterns = [path("", room_views.all_rooms, name="home")]

