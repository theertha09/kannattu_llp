# serializers.py
from rest_framework import serializers
from .models import Resignation

class ResignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resignation
        fields = '__all__'
