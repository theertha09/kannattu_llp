from rest_framework import serializers
from .models import DocumentUpload, DocumentImage
from django.core.files.images import get_image_dimensions
from personaldetails.models import PersonalDetails

class DocumentImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentImage
        fields = ['id', 'image', 'image_url', 'document_type', 'original_filename', 
                 'file_size', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at', 'file_size', 'original_filename']
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class DocumentUploadSerializer(serializers.ModelSerializer):
    images = DocumentImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    document_types = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    user_uuid = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = DocumentUpload
        fields = ['id', 'title', 'images', 'uploaded_images', 'document_types', 'user_uuid',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_user_uuid(self, value):
        """Validate that the PersonalDetails exists with this UUID"""
        try:
            PersonalDetails.objects.get(uuid=value)
            return value
        except PersonalDetails.DoesNotExist:
            raise serializers.ValidationError("PersonalDetails with this UUID does not exist.")
        except Exception as e:
            raise serializers.ValidationError(f"Invalid UUID format: {str(e)}")
    
    def validate_uploaded_images(self, images):
        """Validate each uploaded image"""
        if not images:
            return images
            
        for image in images:
            # Check file size (max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if image.size > max_size:
                raise serializers.ValidationError(f"Image {image.name} is too large. Maximum size is 5MB.")
            
            # Check file format
            allowed_formats = ['JPEG', 'JPG', 'PNG', 'PDF']
            ext = image.name.split('.')[-1].upper()
            if ext not in allowed_formats:
                raise serializers.ValidationError(
                    f"Unsupported file format for {image.name}. Please use JPEG, JPG, PNG, or PDF."
                )
        
        return images
    
    def validate(self, data):
        """Validate that images and document_types have same length"""
        uploaded_images = data.get('uploaded_images', [])
        document_types = data.get('document_types', [])
        
        if uploaded_images and document_types:
            if len(uploaded_images) != len(document_types):
                raise serializers.ValidationError(
                    "Number of images must match number of document types."
                )
        
        # Validate document types
        valid_types = [choice[0] for choice in DocumentImage.DOCUMENT_TYPES]
        for doc_type in document_types:
            if doc_type not in valid_types:
                raise serializers.ValidationError(
                    f"'{doc_type}' is not a valid document type. Choose from: {valid_types}"
                )
        
        return data
    
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        document_types = validated_data.pop('document_types', [])
        user_uuid = validated_data.pop('user_uuid')
        
        try:
            # Get PersonalDetails instance using UUID
            personal_details = PersonalDetails.objects.get(uuid=user_uuid)
            
            # Get or create DocumentUpload instance (since it's OneToOneField)
            document_upload, created = DocumentUpload.objects.get_or_create(
                user=personal_details,
                defaults=validated_data
            )
            
            # If not created, update the title if provided
            if not created and validated_data.get('title'):
                document_upload.title = validated_data['title']
                document_upload.save()
            
            # Create DocumentImage instances
            for i, image in enumerate(uploaded_images):
                document_type = document_types[i] if i < len(document_types) else 'passport'
                
                DocumentImage.objects.create(
                    document_upload=document_upload,
                    image=image,
                    document_type=document_type,
                    original_filename=image.name,
                    file_size=image.size
                )
            
            return document_upload
        
        except PersonalDetails.DoesNotExist:
            raise serializers.ValidationError("PersonalDetails with this UUID does not exist.")
        except Exception as e:
            raise serializers.ValidationError(f"Error creating document upload: {str(e)}")
