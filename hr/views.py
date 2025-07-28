from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import hr
from .serializers import hrSerializer
from roles.models import Role
from django.db.models import Q

class TelecallerPagination(PageNumberPagination):
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

class TelecallerListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', '')

        # You can adjust these fields as per your model
        if search_query:
            telecallers = hr.objects.filter(
                Q(name__icontains=search_query) 
            
            ).order_by('-id')
        else:
            telecallers = hrSerializer.objects.all().order_by('-id')

        paginator = TelecallerPagination()
        result_page = paginator.paginate_queryset(telecallers, request)
        serializer = hrSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


    def post(self, request):
        serializer = hrSerializer(data=request.data)
        if serializer.is_valid():
            telecaller = serializer.save(created_by=request.user)
            return Response({
                "code": 201,
                "message": "Telecaller created successfully",
                "data": hrSerializer(telecaller).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

class TelecallerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return hr.objects.get(pk=pk)
        except hr.DoesNotExist:
            return None

    def get(self, request, pk):
        hr = self.get_object(pk)
        if not hr:
            return Response({
                "code": 404,
                "message": "hr not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = hrSerializer(hr)
        return Response({
            "code": 200,
            "message": "hr fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        telecaller = self.get_object(pk)
        if not telecaller:
            return Response({
                "code": 404,
                "message": "Telecaller not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = hrSerializer(telecaller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": 200,
                "message": "Telecaller updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "code": 400,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        hr = self.get_object(pk)
        if not hr:
            return Response({
                "code": 404,
                "message": "hr not found"
            }, status=status.HTTP_404_NOT_FOUND)

        hr.delete()  

        return Response({
            "code": 204,
            "message": "hr and associated account deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


