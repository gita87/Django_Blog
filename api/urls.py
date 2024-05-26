# urls.py
from django.urls import path
from .views import ImageUploadAPIView, FindImageByFilenameAPIView

urlpatterns = [
    path("upload-image/",
         ImageUploadAPIView.as_view(),
         name="upload-image"),
    # other urlpatterns
    path(
        "find-image/<str:filename>/",
        FindImageByFilenameAPIView.as_view(),
        name="find-image",
    ),
]
