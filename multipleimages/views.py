from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from .models import DocumentUpload, DocumentImage
from .serializers import DocumentUploadSerializer, DocumentImageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from personaldetails.models import PersonalDetails
from .serializers import DocumentUploadSerializer

class DocumentUploadListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentUploadSerializer
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        return DocumentUpload.objects.all()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                document_upload = serializer.save()
                response_serializer = DocumentUploadSerializer(
                    document_upload, 
                    context={'request': request}
                )
                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': f'Failed to upload documents: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DocumentUploadDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentUploadSerializer
    permission_classes = []
    queryset = DocumentUpload.objects.all()

class DocumentImageListView(generics.ListAPIView):
    serializer_class = DocumentImageSerializer
    permission_classes = []
    
    def get_queryset(self):
        return DocumentImage.objects.all()

class DocumentImageDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = DocumentImageSerializer
    permission_classes = []
    queryset = DocumentImage.objects.all()

# Debug view for testing
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def debug_view(request):
    return Response({
        'method': request.method,
        'data': dict(request.data) if hasattr(request, 'data') else {},
        'files': list(request.FILES.keys()) if hasattr(request, 'FILES') else [],
        'content_type': request.content_type,
        'message': 'API is working'
    })



class DocumentUploadByUUIDView(APIView):
    def get(self, request, user_uuid):
        try:
            user = PersonalDetails.objects.get(user_uuid=user_uuid)
            document_upload = DocumentUpload.objects.filter(user=user).first()
            if not document_upload:
                return Response({'detail': 'No documents found for this user.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = DocumentUploadSerializer(document_upload, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except PersonalDetails.DoesNotExist:
            return Response({'error': 'User with this UUID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
