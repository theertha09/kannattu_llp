from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from personaldetails.models import PersonalDetails
from .serializers import PersonalDetailsSerializer, StatusUpdateSerializer
from datetime import datetime


# ✅ Pagination class
class UserDetailsPagination(PageNumberPagination):
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


class AllUsersAndStatusCountView(ListAPIView):
    serializer_class = PersonalDetailsSerializer
    pagination_class = UserDetailsPagination

    def get_queryset(self):
        queryset = PersonalDetails.objects.all().order_by('-created_at')

        # ✅ Filter by full name (exact match)
        full_name = self.request.query_params.get('full_name')
        if full_name:
            queryset = queryset.filter(full_name__iexact=full_name)

        # ✅ Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # ✅ Search by full_name or email (partial match)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) | Q(email__icontains=search)
            )

        # ✅ Filter by start_date (created_at >= start)
        start_date = self.request.query_params.get('start_date')
        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                queryset = queryset.filter(created_at__gte=start)
            except ValueError:
                print("Invalid start_date format. Use YYYY-MM-DD.")

        # ✅ Filter by end_date (created_at <= end of that day)
        end_date = self.request.query_params.get('end_date')
        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d')
                end = end.replace(hour=23, minute=59, second=59)
                queryset = queryset.filter(created_at__lte=end)
            except ValueError:
                print("Invalid end_date format. Use YYYY-MM-DD.")

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        # ✅ Build status summary counts
        STATUS_CHOICES = dict(PersonalDetails._meta.get_field('status').choices)
        status_counts_raw = PersonalDetails.objects.values('status').annotate(count=Count('status'))
        status_counts_dict = {item['status']: item['count'] for item in status_counts_raw}
        full_status_summary = {key: status_counts_dict.get(key, 0) for key in STATUS_CHOICES.keys()}

        # ✅ Return response with status summary
        response = self.get_paginated_response(serializer.data)
        response.data["status_summary"] = full_status_summary
        return response
    
# ✅ Retrieve single user by UUID
class UserDetailByUUIDView(RetrieveAPIView):
    queryset = PersonalDetails.objects.all()
    serializer_class = PersonalDetailsSerializer
    lookup_field = 'uuid'

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)

            # Count users per status
            STATUS_CHOICES = dict(PersonalDetails._meta.get_field('status').choices)
            status_counts_raw = PersonalDetails.objects.values('status').annotate(count=Count('status'))
            status_counts_dict = {item['status']: item['count'] for item in status_counts_raw}
            full_status_summary = {key: status_counts_dict.get(key, 0) for key in STATUS_CHOICES.keys()}

            return Response({
                'user': serializer.data,
                'status_summary': full_status_summary
            }, status=status.HTTP_200_OK)

        except PersonalDetails.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# ✅ PATCH API to update user status
class UserStatusUpdateView(UpdateAPIView):
    queryset = PersonalDetails.objects.all()
    serializer_class = StatusUpdateSerializer
    lookup_field = 'uuid'

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Status updated successfully",
                    "user_uuid": str(instance.uuid),
                    "new_status": serializer.data['status']
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except PersonalDetails.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
