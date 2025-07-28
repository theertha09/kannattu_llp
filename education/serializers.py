# serializers.py

from rest_framework import serializers
from .models import EducationEmployment

class EducationEmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationEmployment
        fields = '__all__'



