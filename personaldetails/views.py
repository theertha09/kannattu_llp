from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import PersonalDetails,ResidentialAddress
from .serializers import PersonalDetailsSerializer,ResidentialAddressSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PersonalDetails
from .serializers import UserDetailSummarySerializer

from rest_framework.permissions import AllowAny

# ✅ Custom Pagination Class
class PersonalPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "code": 200,
            "message": "",
            "data": data,
            "pagination": {
                "total": self.page.paginator.count,
                "page": self.page.number,
                "limit": self.get_page_size(self.request),
                "totalPages": self.page.paginator.num_pages,
            }
        })


# ✅ List API View with Pagination
class PersonalDetailsListAPIView(generics.ListAPIView):
    queryset = PersonalDetails.objects.all()
    serializer_class = PersonalDetailsSerializer
    pagination_class = PersonalPagination


# ✅ Create API View
class PersonalDetailsCreateAPIView(generics.CreateAPIView):
    queryset = PersonalDetails.objects.all()
    serializer_class = PersonalDetailsSerializer


# ✅ Retrieve & Update API View
class PersonalDetailsRetrieveUpdateDestroyByUUIDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonalDetails.objects.all()
    serializer_class = PersonalDetailsSerializer
    lookup_field = 'uuid'  # Use UUID instead of the default pk

class ResidentialAddressCreateView(generics.CreateAPIView):
    queryset = ResidentialAddress.objects.all()
    serializer_class = ResidentialAddressSerializer

class ResidentialAddressListView(generics.ListAPIView):
    queryset = ResidentialAddress.objects.all()
    serializer_class = ResidentialAddressSerializer
    pagination_class = PersonalPagination  # ✅ Add this line

class ResidentialAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResidentialAddress.objects.all()
    serializer_class = ResidentialAddressSerializer
    lookup_field = 'id'

#idcards details
class UserDetailByUUIDView(APIView):
    def get(self, request, user_uuid):
        try:
            user = PersonalDetails.objects.get(uuid=user_uuid)
            serializer = UserDetailSummarySerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PersonalDetails.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# ✅ ID Card Details - PATCH (Update) by UUID
class UserDetailPatchByUUIDView(APIView):
    permission_classes = [AllowAny]  # Use custom permission if needed

    def patch(self, request, user_uuid):
        try:
            user = PersonalDetails.objects.get(uuid=user_uuid)
            serializer = UserDetailSummarySerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "code": 200,
                    "message": "User ID card details updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "code": 400,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except PersonalDetails.DoesNotExist:
            return Response({"code": 404, "error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
