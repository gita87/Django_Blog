# urls.py
from django.urls import path
from .views import ImageUploadAPIView

urlpatterns = [
    path('upload-image/', ImageUploadAPIView.as_view(), name='upload-image'),
    # other urlpatterns
]
