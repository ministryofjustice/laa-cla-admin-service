from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.cla_auth.constants import ExternalRole, InternalRole
from apps.cla_auth.entra_backend import EntraBackend

TENANT_ID = "0000-0000-0000-0000"


class TestEntraAuth(TestCase):
    @patch("apps.cla_auth.entra_backend.settings.TENANT_ID", TENANT_ID)
    def test_create_user(self):
        """Test happy path for creating new user."""

        backend = EntraBackend()
        claims = {
            "tid": TENANT_ID,
            "USER_EMAIL": "test.user@justice.gov.uk",
        }
        user = backend.create_user(claims)
        self.assertEqual(user.username, "test.user")
        self.assertEqual(user.email, claims["USER_EMAIL"])

    @patch("apps.cla_auth.entra_backend.settings.TENANT_ID", TENANT_ID)
    def test_create_user__username_generation(self):
        """Test a username is generated if the user part of the email address is already taken."""

        get_user_model().objects.create_user(
            "test.user", "testuser@justice.gov.uk"
        ).save()
        backend = EntraBackend()
        claims = {
            "tid": TENANT_ID,
            "USER_EMAIL": "test.user@justice.gov.uk",
        }
        user = backend.create_user(claims)
        self.assertEqual(user.username, "test.user1")

    @patch("apps.cla_auth.entra_backend.settings.TENANT_ID", TENANT_ID)
    def test_create_user__incorrect_tenant_id(self):
        """Test that the correct exception is raised if the tenant id in the claim does not match that of our settings."""

        backend = EntraBackend()
        claims = {
            "tid": "1111-1111-1111-1111",
            "USER_EMAIL": "test.user@justice.gov.uk",
        }
        with self.assertRaises(PermissionDenied, msg="Entra - Invalid Tenant ID"):
            backend.create_user(claims)

    @patch("apps.cla_auth.entra_backend.settings.TENANT_ID", TENANT_ID)
    def test_create_user__missing_email(self):
        """Test that the correct exception is raised if the email is missing in the claim."""

        backend = EntraBackend()
        claims = {
            "tid": TENANT_ID,
        }
        with self.assertRaises(
            PermissionDenied, msg="Entra - Email address is required"
        ):
            backend.create_user(claims)

    @patch("apps.cla_auth.entra_backend.settings.GROUPS_CLAIM", "LAA_APP_ROLES")
    @patch("django_entra_auth.backend.AdfsAuthCodeBackend.validate_access_token")
    def test_token_validation(self, mock_validate_access_token):
        mock_validate_access_token.return_value = {
            "LAA_APP_ROLES": f"CLA Admin - {InternalRole.CONTRACT_MANAGER.value}",
        }
        backend = EntraBackend()
        # We don't care about the access token value as we have mocked the return from super
        claims = backend.validate_access_token("access token")
        self.assertEqual(claims["LAA_APP_ROLES"], [InternalRole.CONTRACT_MANAGER.value])

    @patch("apps.cla_auth.entra_backend.settings.GROUPS_CLAIM", "LAA_APP_ROLES")
    @patch("django_entra_auth.backend.AdfsAuthCodeBackend.validate_access_token")
    def test_empty_laa_accounts_without_contract_manager_is_denied(
        self, mock_validate_access_token
    ):
        mock_validate_access_token.return_value = {
            "LAA_APP_ROLES": "CLA Admin - Case Worker",
            "LAA_ACCOUNTS": [],
        }
        backend = EntraBackend()
        with self.assertRaisesRegex(PermissionDenied, "Internal role required"):
            backend.validate_access_token("access token")

    @patch("apps.cla_auth.entra_backend.settings.GROUPS_CLAIM", "LAA_APP_ROLES")
    @patch("django_entra_auth.backend.AdfsAuthCodeBackend.validate_access_token")
    def test_empty_laa_accounts_with_contract_manager_is_allowed(
        self, mock_validate_access_token
    ):
        mock_validate_access_token.return_value = {
            "LAA_APP_ROLES": f"CLA Admin - {InternalRole.CONTRACT_MANAGER.value}",
            "LAA_ACCOUNTS": [],
        }
        backend = EntraBackend()
        claims = backend.validate_access_token("access token")
        self.assertEqual(claims["LAA_APP_ROLES"], [InternalRole.CONTRACT_MANAGER.value])

    @patch("apps.cla_auth.entra_backend.settings.GROUPS_CLAIM", "LAA_APP_ROLES")
    @patch("django_entra_auth.backend.AdfsAuthCodeBackend.validate_access_token")
    def test_laa_accounts_with_invalid_code(self, mock_validate_access_token):
        mock_validate_access_token.return_value = {
            "LAA_APP_ROLES": f"CLA Admin - {ExternalRole.CASE_WORKER.value}",
            "LAA_ACCOUNTS": ["003"],
        }
        backend = EntraBackend()
        with self.assertRaisesRegex(PermissionDenied, "Office code not allowed"):
            backend.validate_access_token("access token")
