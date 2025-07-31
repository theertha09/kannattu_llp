from rest_framework import serializers
from .models import PersonalDetails,ResidentialAddress
from multipleimages.models import DocumentImage
from education.models import EducationEmployment  # if this is where designation is

class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = '__all__'
class ResidentialAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialAddress
        fields = '__all__'
class UserDetailSummarySerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = PersonalDetails
        fields = ['uuid', 'full_name', 'mobile_number', 'date_of_birth', 'blood_group', 'address','emergency_contact_number']

    def get_address(self, obj):
        address_obj = obj.seller_details.first()
        if address_obj:
            return f"{address_obj.address_line}, {address_obj.place}, {address_obj.district}, {address_obj.state}, {address_obj.pin_code}"
        return None


class DocumentImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = DocumentImage
        fields = ['document_type', 'original_filename', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url


class UserDetailSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()
    designation = serializers.SerializerMethodField()

    class Meta:
        model = PersonalDetails
        fields = [
            'uuid', 'full_name', 'application_id', 'email',
            'designation', 'created_at', 'status', 'documents'
        ]

    def get_documents(self, obj):
        if hasattr(obj, 'document_uploads'):
            images = obj.document_uploads.images.all()
            return DocumentImageSerializer(images, many=True, context=self.context).data
        return []

    def get_designation(self, obj):
        try:
            return obj.educationemployment.designation  # If OneToOneField
        except:
            return None
