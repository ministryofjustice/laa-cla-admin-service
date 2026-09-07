from django.core.exceptions import ImproperlyConfigured
from django_entra_auth.config import Settings


class TestEntraSettings(Settings):
    def __init__(self):
        try:
            super().__init__()
        except ImproperlyConfigured:
            # Some settings will be missing when testing
            pass
