import nh3
from django import forms
from django.db import models

class HtmlSanitizedCharField(forms.CharField):
    def to_python(self, value):
        value = super().to_python(value)
        if value not in self.empty_values:
            value = nh3.clean(
                value,
                tags={
                    'a', 'abbr', 'acronym', 'b', 'blockquote',
                    'code', 'em', 'i', 'li', 'ol', 'strong',
                    'ul', 'pre',
                    'h1', 'h2', 'h3', 'p', 'img', 'span', 'figure',
                    'figcaption', 'div', 'br', 'span', 'hr', 'trix-editor'
                    # Add more allowed tags as needed
                },
                attributes={
                    'a': {'href', 'title'},
                    'img': {'src', 'alt', 'style', 'data-trix-mutable',
                            'data-trix-serialized-attributes',
                            'data-trix-store-key', 'data-invert'},
                    'figure': {'contenteditable', 'data-trix-attachment',
                               'data-trix-content-type', 'data-trix-id',
                               'data-trix-attributes', 'data-trix-serialize',
                               'class'},
                    'figcaption': {'class'},
                    'span': {'data-trix-cursor-target', 'data-trix-serialize'},
                    'progress': {'class', 'value', 'max', 'data-trix-mutable',
                                 'data-trix-store-key'},
                    'trix-editor': {'input', 'class', 'role', 'trix-id',
                                    'contenteditable', 'toolbar'}
                    # Add more allowed attributes as needed
                },
            )
        return value

class HtmlSanitizedTextField(models.TextField):
    def formfield(self, form_class=HtmlSanitizedCharField, **kwargs):
        return super().formfield(form_class=form_class, **kwargs)
