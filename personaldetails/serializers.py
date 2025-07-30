from rest_framework import serializers
from .models import PersonalDetails,ResidentialAddress

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
