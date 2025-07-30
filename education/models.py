from django.db import models
from django.conf import settings
from personaldetails.models import PersonalDetails
import os


class EducationEmployment(models.Model):
    user = models.OneToOneField(PersonalDetails, on_delete=models.CASCADE, related_name='education_employment')
    
    highest_qualification = models.CharField(max_length=255)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    pan_number = models.CharField(max_length=10, unique=True)
    previous_employer = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1)
    joining_date = models.DateField()
    branch = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.user.full_name} - {self.highest_qualification}"



