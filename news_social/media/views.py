from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, JSONParser

from media.serializers import MediaSerializer


# Create your views here.


class MediaFileView(CreateAPIView):
    """
    Upload media.
    """
    serializer_class = MediaSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def get_serializer_context(self):
        return {
            "request": self.request,
            "user": self.request.user,
        }
