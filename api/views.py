# views.py
import base64
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import ImageSerializer


class ImageUploadAPIView(APIView):
    def post(self, request, format=None):
        try:
            base64_data = request.data.get("image_data")
            image_url = request.data.get("image_blob")
            image_extension = request.data.get("image_extension")
            print(image_url)
            # Convert base64 data to image
            image = base64.b64decode(base64_data)
            image_filename = f"{image_url.split('/')[-1]}.{image_extension}"
            image_filepath = os.path.join(settings.MEDIA_ROOT, image_filename)

            # Save the image to the file
            with open(image_filepath, "wb") as file:
                file.write(image)

            # Save image information to the database
            image_data = {
                'filename': image_filename,
                'url': f"/media/{image_filename}",
            }
            serializer = ImageSerializer(data=image_data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise Exception(serializer.errors)

            return Response(
                {
                    "success": True,
                    "filename": image_filename,
                    "url": f"/media/{image_filename}"
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
