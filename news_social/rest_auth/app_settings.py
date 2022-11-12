from django.conf import settings

from core.utils import import_callable, default_create_token

create_token = import_callable(
    getattr(settings, "REST_AUTH_TOKEN_CREATOR", default_create_token)
)
