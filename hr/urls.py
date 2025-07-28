from django.urls import path
from .views import (
    TelecallerListCreateView,
    TelecallerDetailView
)

urlpatterns = [
    path('hr/', TelecallerListCreateView.as_view(), name='telecaller-list-create'),
    path('hr/<int:pk>/', TelecallerDetailView.as_view(), name='telecaller-detail'),
]
