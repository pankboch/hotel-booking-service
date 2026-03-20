from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from rooms.models import Room
from rooms.serializers import RoomGetSerializer


@pytest.mark.django_db
def test_get_rooms_returns_all_rooms(api_client: APIClient, rooms: list[Room]) -> None:
    url = reverse("get_all_rooms")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = response.json()
    expected = RoomGetSerializer(rooms, many=True).data

    assert isinstance(actual, list)
    assert len(actual) == len(expected)
    assert actual == expected


@pytest.mark.django_db
def test_get_rooms_returns_empty_list_when_no_rooms(api_client: APIClient) -> None:
    url = reverse("get_all_rooms")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = response.json()
    assert actual == []
