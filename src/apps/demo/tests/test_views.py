from django.http import HttpResponse
from django.test import Client


def test_demo_index_view(client: Client) -> None:
    response = client.get("/")
    assert response.status_code == HttpResponse.status_code
