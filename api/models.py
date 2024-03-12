# models.py
from django.db import models
from django.utils import timezone


class UploadedImage(models.Model):
    filename = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.url or not self.filename:
            # Don't save the instance if url or filename is null
            return

        super().save(*args, **kwargs)
