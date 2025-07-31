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
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]


    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_id = models.CharField(max_length=10, unique=True, blank=True, null=True)  # ONB001 etc.
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    emergency_contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
        # New status field
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )



    def save(self, *args, **kwargs):
        if not self.application_id:
            last_id = PersonalDetails.objects.all().order_by('application_id').last()
            if last_id and last_id.application_id:
                last_number = int(last_id.application_id.replace("ONB", ""))
                new_number = last_number + 1
            else:
                new_number = 1
            self.application_id = f"ONB{new_number:03d}"
        super().save(*args, **kwargs)

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

