# safe_filters.py
from html_sanitizer import Sanitizer
from django import template
import bleach

register = template.Library()

ALLOWED_TAGS = [
    'a', 'img', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'pre',
    'h1', 'h2', 'h3', 'p',  'span', 'figure', 'figcaption', 'div', 'br', 'span', 'hr', 'trix-editor'
    # Tambahkan tag lain yang ingin Anda pertahankan di sini
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'style', 'data-trix-mutable', 'data-trix-serialized-attributes', 'data-trix-store-key'],
    'figure': ['contenteditable', 'data-trix-attachment', 'data-trix-content-type', 'data-trix-id', 'data-trix-attributes', 'data-trix-serialize', 'class'],
    'figcaption': ['class'],
    'span': ['data-trix-cursor-target', 'data-trix-serialize'],
    'progress': ['class', 'value', 'max', 'data-trix-mutable', 'data-trix-store-key'],
    'trix-editor': ['input', 'class', 'role', 'trix-id', 'contenteditable', 'toolbar']
    # ...
}

ALLOWED_STYLES = ['max-width', 'height']  # Tambahkan properti CSS lain yang diizinkan

# Buat objek sanitizer
sanitizer = Sanitizer()

@register.filter(name='sanitize_html')
def sanitize_html(value):
    # Bersihkan HTML menggunakan bleach terlebih dahulu
    linked_value = bleach.linkify(value)
    cleaned_value = bleach.clean(linked_value,
                                 tags=ALLOWED_TAGS,
                                 attributes=ALLOWED_ATTRIBUTES,
                                 strip=True)

    # Hapus atribut gaya menggunakan html_sanitizer
    cleaned_value = sanitizer.sanitize(cleaned_value)

    return cleaned_value
