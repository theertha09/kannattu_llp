# urls.py

from django.urls import path
from .views import (
    EducationEmploymentCreateAPIView,
    EducationEmploymentRetrieveUpdateAPIView,
    
)

urlpatterns = [
    path('education-employment/create/', EducationEmploymentCreateAPIView.as_view(), name='education-create'),
    path('education-employment/<uuid:user_id>/', EducationEmploymentRetrieveUpdateAPIView.as_view(), name='education-detail'),

]
