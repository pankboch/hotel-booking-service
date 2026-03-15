from django.urls import path

from . import views

urlpatterns = [
    path("room/<int:room_id>/", views.BookingsRoomGetView.as_view(), name="all_bookings_for_room"),
    path("delete/<int:booking_id>/", views.BookingDeleteView.as_view(), name="delete_booking"),
]
