from django.db import models

# Create your models here.
from django.db import models
import uuid

class PersonalDetails(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    emergency_contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name


class ResidentialAddress(models.Model):
    user = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name='seller_details')
    address_line = models.CharField(max_length=255)
    village = models.CharField(max_length=100)
    post_office = models.CharField(max_length=100)
    panchayat = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    taluk = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    place = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line} - {self.place}"

