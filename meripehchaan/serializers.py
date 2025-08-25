from rest_framework import serializers

class AuthInitSerializer(serializers.Serializer):
    service = serializers.ChoiceField(choices=["aadhaar_ekyc", "pan_verify"])
    # optional: redirect or extra params if needed
