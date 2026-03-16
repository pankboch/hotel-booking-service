from django.urls import path

from . import views

urlpatterns = [
    path("room/", views.BookingsRoomGetView.as_view(), name="all_bookings_for_room"),
    path("delete/<int:booking_id>/", views.BookingDeleteView.as_view(), name="delete_booking"),
    path("create/", views.BookingAddView.as_view(), name="add_booking"),
]
