from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import nh3
from .mixins import HtmlSanitizedTextField

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HtmlSanitizedTextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.image:
            # Constructing HTML content with the image
            self.content = f'<p><img alt="" src="{self.image.url}" style="max-width:100%; height:auto;"></p>'

            # Sanitize the HTML content
            self.content = self.sanitize_html(self.content)

        super().save(*args, **kwargs)

    def sanitize_html(value):
        # Create a deep copy of ALLOWED_ATTRIBUTES
        attributes = nh3.ALLOWED_ATTRIBUTES.copy()

        # Define additional attributes for each tag
        additional_attributes = {
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'style', 'data-trix-mutable', 'data-trix-serialized-attributes', 'data-trix-store-key', 'data-invert'],
            'span': ['data-trix-cursor-target', 'data-trix-serialize'],
            'progress': ['class', 'value', 'max', 'data-trix-mutable', 'data-trix-store-key'],
            'trix-editor': ['input', 'class', 'role', 'trix-id', 'contenteditable', 'toolbar']
            # Add more allowed attributes as needed
        }

        # Update ALLOWED_ATTRIBUTES with additional attributes
        for tag, attrs in additional_attributes.items():
            attributes[tag] = attributes.get(tag, set()).union(attrs)

        # Clean HTML using nh3
        cleaned_value = nh3.clean(value, attributes=attributes)

        return cleaned_value