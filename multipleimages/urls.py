from django.urls import path
from . import views

urlpatterns = [
    # Document upload endpoints
    path('documents/', views.DocumentUploadListCreateView.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', views.DocumentUploadDetailView.as_view(), name='document-detail'),
    
    # Document image endpoints  
    path('images/', views.DocumentImageListView.as_view(), name='document-images'),
    path('images/<int:pk>/', views.DocumentImageDetailView.as_view(), name='image-detail'),
    
    # Debug endpoint
    path('debug/', views.debug_view, name='debug'),
]
