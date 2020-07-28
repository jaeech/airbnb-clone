from django.urls import path
from rooms import views as room_views

# app_name은  config.urls.py 내에 있는 namespace 명칭과 동일해야함
app_name = "core"

# views에서 생성한 Class를 불러오면서
# .as_view()를 붙여줌으로서 작동하게만듦(function만 불러올 수 있어서)
urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]

