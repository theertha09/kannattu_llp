from django.urls import path
from .views import (
    AllUsersAndStatusCountView,
    UserDetailByUUIDView,
    UserStatusUpdateView
)

urlpatterns = [
    path('users/', AllUsersAndStatusCountView.as_view(), name='all-users'),
    path('users/<uuid:uuid>/', UserDetailByUUIDView.as_view(), name='user-detail'),
    path('users/<uuid:uuid>/status/', UserStatusUpdateView.as_view(), name='user-status-update'),
]
