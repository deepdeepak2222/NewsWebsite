from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from core.aes_encryption_decryption import AESCipher
from rest_auth.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone")
        read_only_fields = "id",

    def validate(self, attrs):
        # Store encrypted password
        password = self.initial_data.get("password")
        if not password:
            raise serializers.ValidationError({
                "password": ["Password is mandatory"]
            })
        attrs["password"] = AESCipher().encrypt(password)
        return attrs

    def create(self, validated_data):
        instance = User.objects.create(**validated_data)
        return instance
