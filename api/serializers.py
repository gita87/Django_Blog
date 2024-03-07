# serializers.py
from rest_framework import serializers
from .models import UploadedImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['filename', 'url', 'uploaded_at']
