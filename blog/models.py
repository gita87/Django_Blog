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

    def sanitize_html(self, value):
        return nh3.clean(
            value,
            tags={
                'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'pre',
                'h1', 'h2', 'h3', 'p', 'img', 'span', 'figure', 'figcaption', 'div', 'br', 'span', 'hr', 'trix-editor'
                # Add more allowed tags as needed
            },
            attributes={
                'a': {'href', 'title'},
                'img': {'src', 'alt', 'style', 'data-trix-mutable', 'data-trix-serialized-attributes', 'data-trix-store-key'},
                'figure': {'contenteditable', 'data-trix-attachment', 'data-trix-content-type', 'data-trix-id', 'data-trix-attributes', 'data-trix-serialize', 'class'},
                'figcaption': {'class'},
                'span': {'data-trix-cursor-target', 'data-trix-serialize'},
                'progress': {'class', 'value', 'max', 'data-trix-mutable', 'data-trix-store-key'},
                'trix-editor': {'input', 'class', 'role', 'trix-id', 'contenteditable', 'toolbar'}
                # Add more allowed attributes as needed
            },
        )
