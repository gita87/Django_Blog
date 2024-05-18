# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UploadedImageSerializer


class ImageUploadAPIView(APIView):
    def post(self, request, format=None):
        try:
            base64_data = request.data.get("data")
            filename = request.data.get("filename")
            extension = request.data.get("extension")

            if not base64_data or not filename:
                raise ValueError(
                    "All 'data', 'extension', and 'filename'" +
                    " fields are required."
                    )

            # Create the image data for the database
            image_data = {
                "filename": filename,
                "data": base64_data,
                "extension": extension
            }

            # Save image information to the database
            serializer = UploadedImageSerializer(data=image_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "filename": filename,
                        "data": base64_data
                     },
                    status=status.HTTP_201_CREATED,
                )
            else:
                raise ValueError(serializer.errors)

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
