from django.urls import path

from . import views

urlpatterns = [
    path("room/<int:room_id>/", views.BookingsRoomGetView.as_view(), name="all_bookings_for_room"),
]
