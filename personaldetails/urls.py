from django.urls import path
from .views import (
    PersonalDetailsListAPIView,
    PersonalDetailsCreateAPIView,
    PersonalDetailsRetrieveUpdateAPIView,
    ResidentialAddressListView,
    ResidentialAddressCreateView,ResidentialAddressDetailView,UserDetailByUUIDView
)

urlpatterns = [
    path('personal-details/', PersonalDetailsListAPIView.as_view(), name='personal-list'),
    path('personal-details/create/', PersonalDetailsCreateAPIView.as_view(), name='personal-create'),
    path('personal-details/<int:id>/', PersonalDetailsRetrieveUpdateAPIView.as_view(), name='personal-update'),
    path('addresses/', ResidentialAddressListView.as_view(), name='address-list'),
    path('addresses/create/', ResidentialAddressCreateView.as_view(), name='address-create'),
    path('addresses/<int:id>/', ResidentialAddressDetailView.as_view(), name='address-detail'),
    path('idcards/<uuid:user_uuid>/', UserDetailByUUIDView.as_view(), name='user-detail-by-uuid'),

]
