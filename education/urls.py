from django.urls import path
from .views import (
    EducationEmploymentCreateAPIView,
    EducationEmploymentRetrieveUpdateAPIView,
    EducationEmploymentListAPIView,
)

urlpatterns = [
    path('education-employment/create/', EducationEmploymentCreateAPIView.as_view(), name='education-create'),
    path('education-employment/<uuid:user_id>/', EducationEmploymentRetrieveUpdateAPIView.as_view(), name='education-detail'),
    path('education-employment/', EducationEmploymentListAPIView.as_view(), name='education-list'),
    path('education-employment/list/<uuid:user_id>/', EducationEmploymentListAPIView.as_view(), name='education-employment-user-list'),

]
