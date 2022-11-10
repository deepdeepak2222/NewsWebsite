from django.db import models
from django_extensions.db.models import TimeStampedModel


class User(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name="User Email", unique=True)
    first_name = models.CharField(null=False, blank=False, max_length=50)
    last_name = models.CharField(null=True, blank=True, max_length=50)
    phone = models.CharField(null=True, blank=True, max_length=15)
    password = models.CharField(null=False, blank=False, max_length=500)
