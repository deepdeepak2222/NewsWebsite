from rest_framework.generics import CreateAPIView

from rest_auth.serializers import UserSerializer


# Create your views here.
class UserSignupView(CreateAPIView):
    serializer_class = UserSerializer
