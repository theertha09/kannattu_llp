from django.urls import path
from .views import (
    PersonalDetailsListAPIView,
    PersonalDetailsCreateAPIView,
    PersonalDetailsRetrieveUpdateDestroyByUUIDAPIView,
    ResidentialAddressListView,
    ResidentialAddressCreateView,ResidentialAddressDetailView,UserDetailByUUIDView,UserDetailPatchByUUIDView
)

urlpatterns = [
    path('personal-details/', PersonalDetailsListAPIView.as_view(), name='personal-list'),
    path('personal-details/create/', PersonalDetailsCreateAPIView.as_view(), name='personal-create'),
    path('personal-details/<uuid:uuid>/', PersonalDetailsRetrieveUpdateDestroyByUUIDAPIView.as_view(), name='personal-update-by-uuid'),
    path('addresses/', ResidentialAddressListView.as_view(), name='address-list'),
    path('addresses/create/', ResidentialAddressCreateView.as_view(), name='address-create'),
    path('address/list/<uuid:user_uuid>/', ResidentialAddressListView.as_view(), name='residential-address-user-list'),

    path('addresses/<int:id>/', ResidentialAddressDetailView.as_view(), name='address-detail'),
    path('idcards/<uuid:user_uuid>/', UserDetailByUUIDView.as_view(), name='user-detail-by-uuid'),
    path('idcards/edit/<uuid:user_uuid>/', UserDetailPatchByUUIDView.as_view(), name='user-detail-edit'),


]
