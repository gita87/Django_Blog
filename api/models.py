# models.py

from django.db import models
from django.utils import timezone


class UploadedImage(models.Model):
    filename = models.CharField(max_length=255)
    data = models.TextField(default='')  # Providing a default value
    extension = models.CharField(
        max_length=10
    )  # Adjust max_length as per your requirement
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.filename
