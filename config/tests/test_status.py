from django.urls import reverse


def test_status_returns_ok(client):
    response = client.get(reverse("status"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}