from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminTestCase(TestCase):
    def test_admin_login_page_is_available(self):
        response = self.client.get(reverse("admin:login"))
        assert response.status_code == 302

    def test_anonymous_user_is_redirected_from_admin_index(self):
        response = self.client.get(reverse("admin:index"))

        assert response.status_code == 302
        assert "/oauth2/login?next=/admin/" in response.url

    def test_superuser_can_access_admin(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.test",
            password="test-password",
        )

        self.client.force_login(user)

        response = self.client.get(reverse("admin:index"))

        assert response.status_code == 200
