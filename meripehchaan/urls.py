# urls.py
from django.urls import path
from .views import AadhaarVerifyAPIView

urlpatterns = [
    path("verify-aadhaar/", AadhaarVerifyAPIView.as_view(), name="verify-aadhaar"),
]
