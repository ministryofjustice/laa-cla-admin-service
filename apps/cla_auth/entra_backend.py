import uuid

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django_entra_auth.backend import AdfsAuthCodeBackend
from django_entra_auth.config import Settings, settings


class EntraSettings(Settings):
    def __init__(self):
        try:
            super(EntraSettings, self).__init__()
        except ImproperlyConfigured as err:
            if not hasattr(django_settings, "TESTING"):
                raise err


class EntraBackend(AdfsAuthCodeBackend):
    def create_user(self, claims):
        """
        Create the user if it doesn't exist yet

        Args:
            claims (dict): claims from the access token

        Returns:
            django.contrib.auth.models.User: A Django user
        """

        # Guard against wrong tenant id
        if claims.get("tid") != settings.TENANT_ID:
            raise PermissionDenied("Entra - Invalid Tenant ID")

        user_model = get_user_model()
        email = claims.get("USER_EMAIL")
        if not email:
            raise PermissionDenied("Entra - Email address is required")

        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            if settings.CREATE_NEW_USERS:
                user_data = {
                    "email": email,
                    user_model.USERNAME_FIELD: self._generate_unique_username(
                        user_model, email
                    ),
                    "is_staff": True,  # This service only caters for admin staff
                    "is_active": True,
                }
                return user_model.objects.create_user(**user_data)
            raise PermissionDenied(
                "Entra - User does not exist and user creation is disabled"
            )
        return user

    @staticmethod
    def _generate_unique_username(user_model, email):
        username_field = getattr(user_model, user_model.USERNAME_FIELD)
        max_length = username_field.field.max_length
        base = email.split("@")[0][:max_length].lower()

        if not user_model.objects.filter(username=base).exists():
            return base

        for counter in range(1, 100):
            suffix = str(counter)
            username = base[: max_length - len(suffix)] + suffix
            if not user_model.objects.filter(username=username).exists():
                return username
        return base[:20] + uuid.uuid4().hex[:7]

    def validate_access_token(self, access_token):
        claims = super().validate_access_token(access_token)

        # Create custom claims for first and last name
        # The format of name is [DEPARTMENT] - [APPLICATION] First Lastname
        names = claims.get("name", "").split("]").pop().strip().split(" ")
        if names:
            claims["CLA_FIRST_NAME"] = names.pop(0)
        if names:
            claims["CLA_LAST_NAME"] = " ".join(names)

        # Make sure claims[settings.GROUPS_CLAIM] is always a list
        if settings.GROUPS_CLAIM in claims and not isinstance(
            claims[settings.GROUPS_CLAIM], list
        ):
            claims[settings.GROUPS_CLAIM] = [claims[settings.GROUPS_CLAIM]]

        # Remove service name prefix from role names
        roles = []
        for role in claims.get(settings.GROUPS_CLAIM, []):
            _, role_name = role.split(" - ")
            roles.append(role_name)
        if roles:
            claims[settings.GROUPS_CLAIM] = roles

        return claims
