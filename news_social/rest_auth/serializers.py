from rest_framework.serializers import ModelSerializer

from rest_auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")
        read_only_fields = "id",

    def create(self, validated_data):
        instance = User.objects.create(**validated_data)
        return instance
