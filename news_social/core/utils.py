from six import string_types
from importlib import import_module

from rest_auth.models import TokenModel
from django.conf import settings


def import_callable(path_or_callable):
    if hasattr(path_or_callable, "__call__"):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit(".", 1)
        return getattr(import_module(package), attr)


def default_create_token(user):
    token = TokenModel.objects.create(user=user)
    return token


def remove_users_previous_sessions(user):
    """Delete previous all tokens of user"""
    sessions = TokenModel.objects.filter(user=user).order_by("-created")
    exclude_allowed_session_ids = list(
        sessions.values_list("pk", flat=True)[:settings.ALLOWED_SESSIONS_AT_A_TIME]
    )
    to_be_deleted_sessions = sessions.exclude(pk__in=exclude_allowed_session_ids)
    to_be_deleted_sessions.delete()


