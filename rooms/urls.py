from django.urls import path
from . import views

app_name = "rooms"

# <int:pk> 를 입력함으로서 url에 입력된 숫자를 pk로 인식해서 가져옴
# html에 넣을 argument는 <int:pk>의 pk가 넘어가는 것
# Detailview에서 자동으로 pk를 끌어가서 view를 설정함
urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]

