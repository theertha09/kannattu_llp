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
from personaldetails.models import PersonalDetails
from personaldetails.serializers import UserDetailSerializer

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
class ResidentialAddressListView(generics.ListAPIView):
    serializer_class = ResidentialAddressSerializer
    pagination_class = PersonalPagination

    def get_queryset(self):
        user_uuid = self.kwargs.get('user_uuid')
        if user_uuid:
            return ResidentialAddress.objects.filter(user__uuid=user_uuid)
        return ResidentialAddress.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "code": 200,
            "message": "",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
class UserDetailByUUIDAPIView(APIView):
    def get(self, request, uuid):
        try:
            user = PersonalDetails.objects.get(uuid=uuid)
        except PersonalDetails.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserDetailSerializer(user, context={'request': request})
        return Response(serializer.data)



class DeleteUserByUUIDAPIView(APIView):
    def delete(self, request, uuid):
        try:
            user = PersonalDetails.objects.get(uuid=uuid)
        except PersonalDetails.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
