from rest_framework import serializers
from personaldetails.models import PersonalDetails, ResidentialAddress
from multipleimages.models import DocumentUpload, DocumentImage
from education.models import EducationEmployment  # If it's in a separate app

# --- Residential Address ---
class ResidentialAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialAddress
        exclude = ['user']

# --- Education Employment ---
class EducationEmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationEmployment
        exclude = ['user']

# --- Document Images ---
class DocumentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentImage
        fields = ['document_type', 'image', 'original_filename', 'file_size', 'uploaded_at']

# --- Document Upload ---
class DocumentUploadSerializer(serializers.ModelSerializer):
    images = DocumentImageSerializer(many=True, read_only=True)

    class Meta:
        model = DocumentUpload
        fields = ['title', 'created_at', 'updated_at', 'images']

# --- Main User Serializer ---
class PersonalDetailsSerializer(serializers.ModelSerializer):
    seller_details = ResidentialAddressSerializer(many=True, read_only=True)
    education_employment = EducationEmploymentSerializer(read_only=True)
    document_uploads = DocumentUploadSerializer(read_only=True)

    class Meta:
        model = PersonalDetails
        fields = '__all__'
class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = ['status']
