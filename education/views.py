from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import EducationEmployment
from .serializers import EducationEmploymentSerializer
from personaldetails.models import PersonalDetails
from rest_framework.pagination import PageNumberPagination

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


# ✅ Create View
class EducationEmploymentCreateAPIView(generics.CreateAPIView):
    queryset = EducationEmployment.objects.all()
    serializer_class = EducationEmploymentSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        if not user_id:
            return Response({"error": "User UUID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(PersonalDetails, uuid=user_id)
        
        if hasattr(user, 'education_employment'):
            return Response(
                {"error": "Education and Employment details already exist for this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Retrieve & Update View
class EducationEmploymentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = EducationEmploymentSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        return EducationEmployment.objects.all()

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(PersonalDetails, uuid=user_id)
        return get_object_or_404(EducationEmployment, user=user)


# ✅ List View with Pagination
class EducationEmploymentListAPIView(generics.ListAPIView):
    queryset = EducationEmployment.objects.all()
    serializer_class = EducationEmploymentSerializer
    pagination_class = PersonalPagination



class EducationEmploymentListAPIView(generics.ListAPIView):
    serializer_class = EducationEmploymentSerializer
    pagination_class = PersonalPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')  # Get UUID from URL if provided
        if user_id:
            user = get_object_or_404(PersonalDetails, uuid=user_id)
            return EducationEmployment.objects.filter(user=user)
        return EducationEmployment.objects.all()

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
