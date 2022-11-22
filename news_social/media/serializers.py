from rest_framework.serializers import ModelSerializer

from media.models import Media


class MediaSerializer(ModelSerializer):
    class Meta:
        fields = ("media_file", "media_id", "uploaded_by", "is_active")
        model = Media
        read_only_fields = ("media_id", "uploaded_by", "is_active")

    def validate(self, attrs):
        attrs["uploaded_by"] = self.context.get("user")
        return attrs

    def create(self, validated_data):
        instance = Media.objects.create(**validated_data)
        return instance

