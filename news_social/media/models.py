import uuid

from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from core.storage import MediaStorage


class Media(TimeStampedModel):
    """
        Default storage model for media/files.
    """
    upload_to = settings.AWS_STORAGE_FOLDER_NAME
    media_id = models.CharField(max_length=250, primary_key=True, default=uuid.uuid4)
    media_file = models.FileField(
        upload_to=upload_to,
        max_length=150,
        # storage=MediaStorage()
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_media",
        on_delete=models.DO_NOTHING
    )
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % self.media_file.name

