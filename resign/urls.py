# urls.py for resignation app

from django.urls import path
from .views import (
    ResignationListCreateAPIView,
    ResignationRetrieveUpdateAPIView,
    ResignationByUserUUIDAPIView,
    UpdateResignationStatusAPIView,
    DeleteResignationAPIView
)

urlpatterns = [
    # GET: List all resignations with filtering and pagination
    # POST: Create new resignation (sends email to HR)
    path('resignations/', ResignationListCreateAPIView.as_view(), name='resignation-list-create'),
    
    # GET: Retrieve specific resignation by UUID
    # PATCH: Update specific resignation by UUID
    path('resignations/<uuid:uuid>/', ResignationRetrieveUpdateAPIView.as_view(), name='resignation-detail'),
    
    # GET: Get all resignations for a specific user UUID
    path('resignations/user/<uuid:user_uuid>/', ResignationByUserUUIDAPIView.as_view(), name='resignation-by-user'),
    
    # PATCH: Update only the status of a resignation
    path('resignations/<uuid:uuid>/status/', UpdateResignationStatusAPIView.as_view(), name='resignation-status-update'),
    
    # DELETE: Delete a resignation by UUID
    path('resignations/<uuid:user_uuid>/delete/', DeleteResignationAPIView.as_view(), name='resignation-delete'),
]