from django.urls import path

from . import views

urlpatterns = [
    path("add/", views.add_booking, name="add_booking"),
    path("delete/", views.delete_booking, name="delete_booking"),
    path("all-bookings-for-room/", views.all_bookings_for_room, name="all_bookings_for_room"),
]
