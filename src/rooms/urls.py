from django.urls import path

from . import views

urlpatterns = [
    path("", views.RoomGetView.as_view(), name="get_all_rooms"),
    path("create", views.RoomCreateView.as_view(), name="add_new_room"),
    path("delete/<int:room_id>/", views.RoomDeleteView.as_view(), name="delete_room"),
]
