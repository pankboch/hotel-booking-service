from django.urls import path

from . import views

urlpatterns = [
    path("add/", views.create_room, name="add_room"),
    path("delete/", views.delete_room, name="delete_room"),
    path("all-rooms/", views.get_rooms, name="all_rooms"),
]
