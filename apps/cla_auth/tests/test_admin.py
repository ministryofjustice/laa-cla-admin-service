import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_admin_login_page_is_available(client):
    response = client.get(reverse("admin:login"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_anonymous_user_is_redirected_from_admin_index(client):
    response = client.get(reverse("admin:index"))

    assert response.status_code == 302
    assert reverse("admin:login") in response.url


@pytest.mark.django_db
def test_superuser_can_access_admin(client, django_user_model):
    user = django_user_model.objects.create_superuser(
        username="admin",
        email="admin@example.test",
        password="test-password",
    )

    client.force_login(user)

    response = client.get(reverse("admin:index"))

    assert response.status_code == 200