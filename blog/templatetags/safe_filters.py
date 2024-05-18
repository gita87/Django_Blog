# safe_filters.py
from copy import deepcopy
import nh3
from django import template
from django.template.defaultfilters import stringfilter
from bs4 import BeautifulSoup
from blog.models import UploadedImage


register = template.Library()

# Create a deep copy of ALLOWED_ATTRIBUTES
attributes = deepcopy(nh3.ALLOWED_ATTRIBUTES)

# Define additional attributes for each tag
allowed_attributes = {
    "a": ["href", "title"],
    "img": [
        "src",
        "alt",
        "style",
        "data-trix-mutable",
        "data-trix-serialized-attributes",
        "data-trix-store-key",
    ],
    # 'figure': ['contenteditable', 'data-trix-attachment', 'data-trix-content-type', 'data-trix-id', 'data-trix-attributes', 'data-trix-serialize', 'class'],
    # 'figcaption': ['class'],
    "span": ["data-trix-cursor-target", "data-trix-serialize"],
    # 'progress': ['class', 'value', 'max', 'data-trix-mutable', 'data-trix-store-key'],
    "trix-editor": ["input", "class", "role", "trix-id", "contenteditable", "toolbar"],
    # Add more allowed attributes as needed
}

# Update ALLOWED_ATTRIBUTES with additional attributes
for tag, attrs in allowed_attributes.items():
    attributes[tag] = attributes.get(tag, set()).union(attrs)


@register.filter(name="sanitize_html")
def sanitize_html(value):
    # Clean HTML using nh3
    cleaned_value = nh3.clean(value, attributes=attributes)
    return cleaned_value


@register.filter(name="remove_figcaption")
def remove_figcaption(html):
    # Parse the HTML content
    soup = BeautifulSoup(html, "html.parser")

    # Find all figcaption tags and remove them
    for figcaption in soup.find_all("figcaption"):
        figcaption.decompose()

    # Return the modified HTML
    return str(soup)


@register.filter(name="replace_img_src_with_base64")
def replace_img_src_with_base64(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    for img in soup.find_all("img"):
        # Extract the trix-store-key
        trix_key = img.get("data-trix-store-key")
        if trix_key:

            # Extract the filename from the trix-key
            filename = trix_key.split("/")[-3]

            # Query the base64 data from the database using the filename
            try:
                uploaded_image = UploadedImage.objects.get(filename=filename)
                base64_data = (
                    uploaded_image.data
                )  # Assuming 'data' field stores the base64 content
                if base64_data:
                    img["src"] = base64_data
            except UploadedImage.DoesNotExist:
                pass
    return str(soup)


@register.filter(name="replace_urls")
@stringfilter
def replace_urls(value, replacements):
    for old_url, new_url in replacements.items():
        value = value.replace(old_url, new_url)
    return value
