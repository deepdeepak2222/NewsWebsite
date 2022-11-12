from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.aes_encryption_decryption import AESCipher
from core.constants import INVALID_REQUEST, USER_NOT_FOUND, WRONG_PASSWORD, AUTH_RESPONSE_CODE
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


class LoginSerializer(serializers.Serializer):
    """
        This serializer defines two fields for authentication:
          * username
          * password.
        It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            try:
                user = User.objects.get(email=username)
                user_password = AESCipher().decrypt(user.password)
                if user_password != password:
                    msg = {
                        "login": [WRONG_PASSWORD]
                    }
                    raise serializers.ValidationError(msg, code=AUTH_RESPONSE_CODE)
                attrs["user"] = user
            except User.DoesNotExist:
                msg = {
                    "login": [USER_NOT_FOUND]
                }
                raise serializers.ValidationError(msg, code=AUTH_RESPONSE_CODE)
            except Exception as e:
                msg = {
                    "detail": [INVALID_REQUEST]
                }
                raise serializers.ValidationError(msg, code=AUTH_RESPONSE_CODE)
        else:
            msg = {
                "detail": ["Both, username and password are required."]
            }
            raise serializers.ValidationError(msg, code=AUTH_RESPONSE_CODE)
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
