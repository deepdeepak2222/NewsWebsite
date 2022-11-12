from django.conf import settings
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from core.utils import default_create_token, remove_users_previous_sessions
from rest_auth.serializers import UserSerializer, LoginSerializer


class UserLoginView(CreateAPIView):
    """
        API: Login
        API Types: POST
        More:
            This view should be accessible also for unauthenticated users.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(
            data=self.request.data,
            context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        self.login(request, user)
        login_response = self.get_login_response()
        return Response(login_response, status=status.HTTP_202_ACCEPTED)

    def login(self, request, user):
        token = default_create_token(user)
        setattr(self, "token", token)
        setattr(self, "user", user)
        if getattr(settings, "REST_SESSION_LOGIN", True):
            login(self.request, self.user)

    def get_login_response(self):
        remove_users_previous_sessions(self.user)
        return {
            "key": self.token.key
        }


class UserSignupView(CreateAPIView):
    """
        API: Signup
        API Types: POST
        More:
            This view should be accessible also for unauthenticated users.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class UserProfileView(ListAPIView):
    """
        API: Get User profile
        API Types: GET
    """
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
