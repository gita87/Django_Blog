from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from bs4 import BeautifulSoup
from api.models import UploadedImage  # Import UploadedImage model
import re


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})

    @staticmethod
    def extract_uuid_from_string(input_string):
        # Define a regular expression pattern to match the UUID
        uuid_pattern = re.compile(r'imageElement/\d+/blob:http://\S+/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/\d+/\d+')

        # Search for the pattern in the input string
        match = uuid_pattern.search(input_string)

        # If a match is found, return the extracted UUID, otherwise return None
        if match:
            return match.group(1)
        else:
            return None

    @staticmethod
    def replace_blob_urls(html_content):
        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all image elements with data-trix-store-key attribute
        image_elements = soup.find_all('img', {'data-trix-store-key': True})
        print("image_elements : ", image_elements)
        # Find all image elements with src attribute starting with blob
        for img in image_elements:
            # Extract UUID from the blob URL
            uuid = Post.extract_uuid_from_string(str(img))

            print(uuid)

            if uuid:
                # Search for matching UUID in the UploadedImage table
                matching_image = UploadedImage.objects.filter(
                    filename__startswith=uuid
                )

                print(matching_image)

                if matching_image:
                    # Replace the src attribute with the UploadedImage URL
                    img['src'] = matching_image[0].url

        # Find all figure elements containing images
        figure_elements = soup.find_all('figure')

        # Loop through each figure element
        for figure in figure_elements:
            # Unwrap the figure element and keep its children
            figure.unwrap()

        # Find and remove all figcaption elements
        figcaption_elements = soup.find_all('figcaption')
        for figcaption in figcaption_elements:
            figcaption.decompose()

        return str(soup)
